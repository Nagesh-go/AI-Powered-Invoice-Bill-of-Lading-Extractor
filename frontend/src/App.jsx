import React, { useState, useEffect } from "react";
import {
  ArrowLeft,
  Bell,
  Sparkles,
  ShieldCheck,
  Cpu,
  Globe2,
} from "lucide-react";

import Sidebar from "./components/Sidebar";
import Stepper from "./components/Stepper";
import DocumentViewer from "./components/DocumentViewer";
import ExtractedFieldsList from "./components/ExtractedFieldsList";
import StatusSidebar from "./components/StatusSidebar";
import { extractDocument, checkBackendHealth } from "./api";

export default function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [pipelineStatus, setPipelineStatus] = useState("idle"); // 'idle' | 'scanning' | 'extracting' | 'completed' | 'error'
  const [progressPercent, setProgressPercent] = useState(0);
  const [globalError, setGlobalError] = useState("");
  const [apiOnline, setApiOnline] = useState(null);

  // Check backend connectivity on mount
  useEffect(() => {
    checkBackendHealth()
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  const handleFileSelect = async (selectedFile) => {
    if (!selectedFile) return;

    setFile(selectedFile);
    setResults(null);
    setGlobalError("");
    setPipelineStatus("scanning");
    setProgressPercent(25);

    // Simulate realistic visual progression through the steps
    const timer1 = setTimeout(() => {
      setPipelineStatus("extracting");
      setProgressPercent(60);
    }, 700);

    try {
      const data = await extractDocument(selectedFile);
      setResults(data);
      setPipelineStatus("completed");
      setProgressPercent(100);
    } catch (err) {
      console.error("Extraction failed:", err);
      setGlobalError(err.message || "An unexpected error occurred during extraction.");
      setPipelineStatus("error");
      setProgressPercent(30);
    } finally {
      clearTimeout(timer1);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResults(null);
    setPipelineStatus("idle");
    setProgressPercent(0);
    setGlobalError("");
  };

  // Determine current step index for the horizontal stepper
  let currentStep = 1; // 1 = Upload
  if (pipelineStatus === "scanning") currentStep = 2; // Scan
  if (pipelineStatus === "extracting") currentStep = 3; // Extract
  if (pipelineStatus === "completed") currentStep = 4; // Review

  return (
    <div className="flowparse-layout">
      {/* 1. Left SaaS Navigation Sidebar */}
      <Sidebar activeNav="documents" />

      {/* 2. Main Content Viewport */}
      <div className="flowparse-main">
        {/* Top Header Bar */}
        <header className="flowparse-header">
          <div className="header-left">
            <button
              type="button"
              className="btn-back"
              onClick={handleReset}
              title="Reset view"
            >
              <ArrowLeft size={18} />
            </button>
            <h2 className="header-title">
              {results?.document_type === "bill_of_lading"
                ? "Bill of Lading Processing"
                : "Invoice Processing"}
            </h2>
          </div>

          {/* Stepper Navigation */}
          <div className="header-center">
            <Stepper currentStep={currentStep} />
          </div>

          {/* User Controls & API Status */}
          <div className="header-right">
            {apiOnline === false && (
              <span className="api-status-chip offline">API Offline</span>
            )}
            {apiOnline === true && (
              <span className="api-status-chip online">API Connected</span>
            )}
            <button type="button" className="icon-btn-round" title="Notifications">
              <Bell size={18} />
            </button>
            <button type="button" className="btn-workspace-pill">
              DocuFlow Pro
            </button>
          </div>
        </header>

        {/* Global Error Banner */}
        {globalError && (
          <div className="alert-banner-error">
            <strong>Extraction Error:</strong> {globalError}
          </div>
        )}

        {/* 3. Three-Column Workspace */}
        <div className="workspace-columns">
          {/* Column 1: Document Preview / Scanner */}
          <div className="col-document">
            <DocumentViewer
              file={file}
              isScanning={pipelineStatus === "scanning" || pipelineStatus === "extracting"}
              onFileSelect={handleFileSelect}
            />
          </div>

          {/* Column 2: Extracted Data Table */}
          <div className="col-extracted">
            <ExtractedFieldsList
              response={results}
              isLoading={pipelineStatus === "scanning" || pipelineStatus === "extracting"}
            />
          </div>

          {/* Column 3: Status, Timeline & Actions */}
          <div className="col-status">
            <StatusSidebar
              file={file}
              status={pipelineStatus}
              progress={progressPercent}
              response={results}
              onReset={handleReset}
            />
          </div>
        </div>

        {/* 4. Bottom Feature Highlights Banner */}
        <footer className="flowparse-bottom-banner">
          <div className="banner-brand-left">
            <div className="banner-icon-box">
              <Sparkles size={20} />
            </div>
            <div>
              <h5>Intelligent Extraction Powered by Google Gemini & Pydantic</h5>
              <p>
                Automatically parses multi-page documents, extracts key commercial entities,
                and validates financial decimals with zero hallucination.
              </p>
            </div>
          </div>

          <div className="banner-pills-right">
            <span className="feature-pill">
              <ShieldCheck size={14} /> High accuracy extraction
            </span>
            <span className="feature-pill">
              <Cpu size={14} /> Smart field detection
            </span>
            <span className="feature-pill">
              <Globe2 size={14} /> Multi-language support
            </span>
          </div>
        </footer>
      </div>
    </div>
  );
}
