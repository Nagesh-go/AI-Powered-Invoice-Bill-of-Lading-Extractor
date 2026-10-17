import React from "react";
import {
  Layers,
  LayoutDashboard,
  FileText,
  FileCode,
  ListFilter,
  GitBranch,
  Download,
  Settings,
  HelpCircle,
} from "lucide-react";

export default function Sidebar({ activeNav = "documents" }) {
  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "documents", label: "Documents", icon: FileText, active: true },
    { id: "templates", label: "Templates", icon: FileCode },
    { id: "fields", label: "Fields", icon: ListFilter },
    { id: "workflows", label: "Workflows", icon: GitBranch },
    { id: "exports", label: "Exports", icon: Download },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside className="app-sidebar">
      {/* Top Brand Logo */}
      <div className="sidebar-brand">
        <div className="brand-icon-box">
          <Layers size={20} className="brand-icon" />
        </div>
        <span className="brand-name">DocuFlow</span>
      </div>

      {/* Main Navigation Links */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = item.id === activeNav;
          return (
            <button
              key={item.id}
              className={`nav-link ${isActive ? "active" : ""}`}
              type="button"
            >
              <Icon size={18} className="nav-icon" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Bottom Profile & Help */}
      <div className="sidebar-footer">
        <button className="nav-link footer-link" type="button">
          <HelpCircle size={18} className="nav-icon" />
          <span>Help & Docs</span>
        </button>

        <div className="user-profile-badge">
          <div className="avatar-circle">JS</div>
          <div className="user-meta">
            <span className="user-name">John Smith</span>
            <span className="user-role">Administrator</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
