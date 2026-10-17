import React from "react";
import { UploadCloud, Scan, Sparkles, CheckSquare, Download } from "lucide-react";

export default function Stepper({ currentStep = 1 }) {
  const steps = [
    { num: 1, label: "Upload", icon: UploadCloud },
    { num: 2, label: "Scan", icon: Scan },
    { num: 3, label: "Extract", icon: Sparkles },
    { num: 4, label: "Review", icon: CheckSquare },
    { num: 5, label: "Export", icon: Download },
  ];

  return (
    <div className="workflow-stepper">
      {steps.map((step, idx) => {
        const Icon = step.icon;
        const isCompleted = step.num < currentStep;
        const isCurrent = step.num === currentStep;

        return (
          <React.Fragment key={step.num}>
            <div
              className={`step-item ${isCompleted ? "completed" : ""} ${
                isCurrent ? "current" : ""
              }`}
            >
              <div className="step-bubble">
                <Icon size={14} />
              </div>
              <span className="step-label">{step.label}</span>
            </div>
            {idx < steps.length - 1 && (
              <div
                className={`step-connector ${
                  step.num < currentStep ? "completed" : ""
                }`}
              />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}
