import React from 'react';

interface SidebarButtonProps {
  icon: React.ReactNode;
  label: string;
  active: boolean;
  expanded: boolean;
  onClick: () => void;
}

export default function SidebarButton({
  icon,
  label,
  active,
  expanded,
  onClick,
}: SidebarButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-3 w-full p-3 rounded-lg transition-colors 
        ${active ? 'bg-blue-100 text-blue-700 font-semibold' : 'hover:bg-gray-100 text-gray-700'}
      `}
    >
      <span className="text-xl">{icon}</span>
      {expanded && <span className="truncate">{label}</span>}
    </button>
  );
}
