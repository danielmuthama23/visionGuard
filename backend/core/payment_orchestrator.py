# core/payment_orchestrator.py
from hedera import AccountBalanceQuery, Hbar, TransferTransaction
from blockchain.nft_minting import HederaNFTHandler
from azure.servicebus import ServiceBusClient
import asyncio

class PaymentOrchestrator:
    def __init__(self):
        self.nft_handler = HederaNFTHandler()
        self.sb_client = ServiceBusClient.from_connection_string(
            os.getenv("SERVICE_BUS_CONN_STR"))
        self._init_queues()

    def _init_queues(self):
        self.payment_queue = self.sb_client.get_queue_receiver("parking-payments")
        self.results_queue = self.sb_client.get_queue_sender("payment-results")

    async def process_payment(self, vehicle_data):
        try:
            # Mint NFT
            nft_id = await self.nft_handler.mint_parking_nft(vehicle_data)
            
            # Create payment transaction
            transfer_tx = TransferTransaction()\
                .addHbarTransfer(
                    vehicle_data['user_account'], 
                    Hbar(-vehicle_data['amount'])
                )\
                .addHbarTransfer(
                    self.nft_handler.treasury_account, 
                    Hbar(vehicle_data['amount'])
                )
            
            # Submit transaction
            tx_id = await transfer_tx.executeAsync(self.nft_handler.client)
            receipt = await tx_id.getReceiptAsync(self.nft_handler.client)
            
            return {
                "success": True,
                "nft_id": nft_id.toString(),
                "tx_hash": receipt.transactionHash.toString()
            }
            
        except Exception as e:
            logger.error(f"Payment failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def listen_for_payments(self):
        async with self.payment_queue:
            while True:
                msg = await self.payment_queue.receive_message()
                vehicle_data = json.loads(str(msg))
                result = await self.process_payment(vehicle_data)
                await self.results_queue.send_messages(
                    ServiceBusMessage(json.dumps(result)))
                await self.payment_queue.complete_message(msg)

    async def validate_nft_payment(self, nft_id):
        try:
            balance = await AccountBalanceQuery()\
                .setAccountId(vehicle_data['user_account'])\
                .executeAsync(self.nft_handler.client)
            
            if balance.hbars < Hbar.fromTinybars(1000):
                raise InsufficientBalanceError()
            
            return await self.nft_handler.validate_nft_ownership(nft_id)
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return False