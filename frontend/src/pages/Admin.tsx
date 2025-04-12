import { AlertBanner, ParkingConfigForm } from "@/components";
import type { ParkingConfig } from "@/components/forms/ParkingConfigForm";

export const Admin = () => {
  const handleSubmit = (data: ParkingConfig) => {
    console.log("Config updated:", data);
    // API call implementation
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-foreground">System Administration</h1>
      
      <AlertBanner
        severity="warning"
        message="Administrative changes will affect live operations"
        className="mb-6"
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-6 bg-background rounded-xl border">
          <h2 className="text-lg font-semibold mb-4">Parking Configuration</h2>
          <ParkingConfigForm onSubmit={handleSubmit} />
        </div>

        {/* ... rest of the component ... */}
      </div>
    </div>
  );
};