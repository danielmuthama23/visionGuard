// src/components/forms/ParkingConfigForm.tsx
import { useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Skeleton } from "@/components/ui/skeleton"

interface ParkingConfigFormProps {
  onSubmit: (data: ParkingConfig) => void
  loading?: boolean
}

export interface ParkingConfig {
  baseRate: number
  capacity: number
  peakMultiplier: number
}

export const ParkingConfigForm = ({ 
  onSubmit,
  loading = false
}: ParkingConfigFormProps) => {
  const { register, handleSubmit } = useForm<ParkingConfig>()

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="space-y-2">
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-10 w-full" />
        </div>
        <div className="space-y-2">
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-10 w-full" />
        </div>
        <div className="space-y-2">
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-10 w-full" />
        </div>
        <Skeleton className="h-10 w-full" />
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="baseRate">Base Rate (USD)</Label>
        <Input
          id="baseRate"
          type="number"
          step="0.01"
          {...register("baseRate", { 
            valueAsNumber: true,
            required: "Base rate is required"
          })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="capacity">Total Capacity</Label>
        <Input
          id="capacity"
          type="number"
          {...register("capacity", {
            valueAsNumber: true,
            required: "Capacity is required",
            min: 1
          })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="peakMultiplier">Peak Multiplier</Label>
        <Input
          id="peakMultiplier"
          type="number"
          step="0.1"
          {...register("peakMultiplier", {
            valueAsNumber: true,
            required: "Multiplier is required",
            min: 1
          })}
        />
      </div>

      <Button type="submit" className="w-full">
        Save Configuration
      </Button>
    </form>
  )
}