// src/components/AlertBanner.tsx
import { cn } from "@/lib/utils";
import { AlertTriangle, CheckCircle2, Info, X } from "lucide-react";

interface AlertBannerProps {
  message: string;
  severity?: "info" | "success" | "warning" | "error";
  className?: string;
}

export const AlertBanner = ({
  message,
  severity = "info",
  className
}: AlertBannerProps) => {
  const iconMap = {
    info: <Info className="h-5 w-5" />,
    success: <CheckCircle2 className="h-5 w-5" />,
    warning: <AlertTriangle className="h-5 w-5" />,
    error: <AlertTriangle className="h-5 w-5" />,
  };

  const colorMap = {
    info: "bg-blue-50 border-blue-200 text-blue-800",
    success: "bg-green-50 border-green-200 text-green-800",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
    error: "bg-red-50 border-red-200 text-red-800",
  };

  return (
    <div className={cn(
      "p-4 rounded-lg border flex items-center gap-3",
      colorMap[severity],
      className
    )}>
      {iconMap[severity]}
      <span className="text-sm">{message}</span>
    </div>
  );
};