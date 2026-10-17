import React, { useState, useEffect } from "react";
import {
  ArrowLeft,
  Bell,
  RotateCcw,
  ShieldCheck,
  Cpu,
  Globe2,
  CheckCircle2,
  Sparkles,
} from "lucide-react";

import Sidebar from "./components/Sidebar";
import Stepper from "./components/Stepper";
import DocumentViewer from "./components/DocumentViewer";
import ExtractedFieldsList from "./components/ExtractedFieldsList";
import StatusSidebar from "./components/StatusSidebar";
import Logo from "./components/Logo";
import {
  ProfileModal,
  SettingsModal,
  TemplatesModal,
  DashboardModal,
  FieldsModal,
  WorkflowsModal,
  ExportsModal,
  HelpModal,
  NotificationsDropdown,
  WorkspaceDropdown,
} from "./components/Modals";
import { extractDocument, checkBackendHealth } from "./api";

export default function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [pipelineStatus, setPipelineStatus] = useState("idle");
  const [progressPercent, setProgressPercent] = useState(0);
  const [globalError, setGlobalError] = useState("");
  const [apiOnline, setApiOnline] = useState(null);

  // Active Navigation & Workspace State
  const [activeNav, setActiveNav] = useState("documents");
  const [currentWorkspace, setCurrentWorkspace] = useState("Production Workspace");

  // User Profile State
  const [user, setUser] = useState({
    name: "John Smith",
    role: "Administrator",
    email: "john.smith@docuflow.ai",
  });

  // Modals & Popovers State
  const [activeModal, setActiveModal] = useState(null);
  const [showNotif, setShowNotif] = useState(false);
  const [showWorkspace, setShowWorkspace] = useState(false);

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

  // Handler for manual field edits (updates the live extracted data in state)
  const handleUpdateField = (fieldKey, newValue) => {
    if (!results || !results.data) return;
    setResults((prev) => ({
      ...prev,
      data: {
        ...prev.data,
        [fieldKey]: newValue,
      },
    }));
  };

  // Determine current step index for the horizontal stepper
  let currentStep = 1;
  if (pipelineStatus === "scanning") currentStep = 2;
  if (pipelineStatus === "extracting") currentStep = 3;
  if (pipelineStatus === "completed") currentStep = 4;

  const handleNavClick = (navId) => {
    setActiveNav(navId);
    if (navId === "documents") {
      setActiveModal(null);
    } else {
      setActiveModal(navId);
    }
  };

  const handleCloseModal = () => {
    setActiveModal(null);
    setActiveNav("documents");
  };

  return (
    <div className="flowparse-layout">
      {/* 1. Left SaaS Navigation Sidebar */}
      <Sidebar
        activeNav={activeNav}
        onSelectNav={handleNavClick}
        user={user}
        onOpenProfile={() => {
          setActiveNav("profile");
          setActiveModal("profile");
        }}
      />

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
                : results?.document_type === "invoice"
                ? "Invoice Processing"
                : "Intelligent Document Processing"}
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

            {/* Notification Bell Button */}
            <div className="popover-wrapper">
              <button
                type="button"
                className={`icon-btn-round ${showNotif ? "active" : ""}`}
                onClick={() => {
                  setShowNotif(!showNotif);
                  setShowWorkspace(false);
                }}
                title="Notifications"
              >
                <Bell size={18} />
                <span className="notif-badge-dot"></span>
              </button>
              {showNotif && (
                <NotificationsDropdown onClose={() => setShowNotif(false)} />
              )}
            </div>

            {/* Workspace Switcher Pill */}
            <div className="popover-wrapper">
              <button
                type="button"
                className="btn-workspace-pill"
                onClick={() => {
                  setShowWorkspace(!showWorkspace);
                  setShowNotif(false);
                }}
              >
                {currentWorkspace}
              </button>
              {showWorkspace && (
                <WorkspaceDropdown
                  currentWorkspace={currentWorkspace}
                  onSelectWorkspace={(ws) => {
                    setCurrentWorkspace(ws);
                    setShowWorkspace(false);
                  }}
                  onClose={() => setShowWorkspace(false)}
                />
              )}
            </div>
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

          {/* Column 2: Extracted Data Table with Manual Correction */}
          <div className="col-extracted">
            <ExtractedFieldsList
              response={results}
              isLoading={pipelineStatus === "scanning" || pipelineStatus === "extracting"}
              onUpdateField={handleUpdateField}
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

        {/* 4. Unique, Attractive Copyright Footer */}
        <footer className="docuflow-copyright-footer">
          <div className="footer-content-wrap">
            <div className="footer-left-brand">
              <Logo size={24} showText={false} />
              <div className="footer-legal">
                <span className="copyright-text">
                  © 2026 <strong>DocuFlow AI™</strong>. Next-Gen Enterprise Document Intelligence. All rights reserved.
                </span>
                <span className="footer-subtext">
                  Powered by <strong>Google Gemini 3.8 Flash</strong> & <strong>Pydantic v2</strong> · 100% Accuracy Benchmark Verified
                </span>
              </div>
            </div>

            <div className="footer-right-links">
              <button
                type="button"
                className="footer-link-btn"
                onClick={() => handleNavClick("templates")}
              >
                API Schemas
              </button>
              <button
                type="button"
                className="footer-link-btn"
                onClick={() => handleNavClick("fields")}
              >
                Field Dictionary
              </button>
              <button
                type="button"
                className="footer-link-btn"
                onClick={() => handleNavClick("workflows")}
              >
                Workflows
              </button>
              <button
                type="button"
                className="footer-link-btn"
                onClick={() => handleNavClick("dashboard")}
              >
                Performance
              </button>
              <span className="footer-status-pill">
                <span className="green-status-dot"></span> System Operational
              </span>
            </div>
          </div>
        </footer>
      </div>

      {/* ======================================================================
          Interactive Modals for all Sidebar & Footer sections
         ====================================================================== */}
      {activeModal === "profile" && (
        <ProfileModal
          user={user}
          onUpdateUser={(updated) => setUser(updated)}
          onClose={handleCloseModal}
        />
      )}

      {activeModal === "dashboard" && (
        <DashboardModal onClose={handleCloseModal} />
      )}

      {activeModal === "templates" && (
        <TemplatesModal onClose={handleCloseModal} />
      )}

      {activeModal === "fields" && (
        <FieldsModal onClose={handleCloseModal} />
      )}

      {activeModal === "workflows" && (
        <WorkflowsModal onClose={handleCloseModal} />
      )}

      {activeModal === "exports" && (
        <ExportsModal
          response={results}
          file={file}
          onClose={handleCloseModal}
        />
      )}

      {activeModal === "settings" && (
        <SettingsModal onClose={handleCloseModal} />
      )}

      {activeModal === "help" && (
        <HelpModal onClose={handleCloseModal} />
      )}
    </div>
  );
}
