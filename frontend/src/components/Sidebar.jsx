import React from "react";
import {
  LayoutDashboard,
  FileText,
  FileCode,
  ListFilter,
  GitBranch,
  Download,
  Settings,
  HelpCircle,
} from "lucide-react";
import Logo from "./Logo";

export default function Sidebar({
  activeNav = "documents",
  onSelectNav,
  user,
  onOpenProfile,
}) {
  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "documents", label: "Documents", icon: FileText },
    { id: "templates", label: "Templates", icon: FileCode },
    { id: "fields", label: "Fields", icon: ListFilter },
    { id: "workflows", label: "Workflows", icon: GitBranch },
    { id: "exports", label: "Exports", icon: Download },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  const initials = user?.name
    ? user.name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .substring(0, 2)
        .toUpperCase()
    : "JS";

  return (
    <aside className="app-sidebar">
      {/* Top Unique Attractive Brand Logo */}
      <div className="sidebar-brand">
        <Logo size={36} showText={true} />
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
              onClick={() => onSelectNav(item.id)}
            >
              <Icon size={18} className="nav-icon" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Bottom Profile & Help (Interactive!) */}
      <div className="sidebar-footer">
        <button
          className="nav-link footer-link"
          type="button"
          onClick={() => onSelectNav("help")}
        >
          <HelpCircle size={18} className="nav-icon" />
          <span>Help & Docs</span>
        </button>

        {/* Interactive User Profile Button */}
        <button
          type="button"
          className="user-profile-badge interactive"
          onClick={onOpenProfile}
          title="Click to view & edit profile"
        >
          <div className="avatar-circle">{initials}</div>
          <div className="user-meta">
            <span className="user-name">{user?.name || "John Smith"}</span>
            <span className="user-role">{user?.role || "Administrator"}</span>
          </div>
        </button>
      </div>
    </aside>
  );
}
