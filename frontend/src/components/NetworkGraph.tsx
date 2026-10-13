import React, { useState, useRef } from 'react';
import { Vertex, Edge, MSTEdge } from '../types';
import { Move, Maximize2, RotateCcw } from 'lucide-react';

interface Props {
  vertices: Vertex[];
  edges: Edge[];
  highlightedEdges?: MSTEdge[] | Edge[];
  highlightPath?: string[]; // ordered vertex IDs for tour or shortest path
  onNodeSelect?: (vertexId: string) => void;
  selectedNodeId?: string | null;
  height?: number;
}

export const NetworkGraph: React.FC<Props> = ({
  vertices,
  edges,
  highlightedEdges = [],
  highlightPath = [],
  onNodeSelect,
  selectedNodeId,
  height = 420
}) => {
  // Local draggable coordinates map
  const [positions, setPositions] = useState<Record<string, { x: number; y: number }>>(() => {
    const pos: Record<string, { x: number; y: number }> = {};
    vertices.forEach((v, idx) => {
      pos[v.id] = {
        x: v.x || 100 + (idx % 4) * 200,
        y: v.y || 100 + Math.floor(idx / 4) * 120
      };
    });
    return pos;
  });

  const [draggingNode, setDraggingNode] = useState<string | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);

  // Sync positions when vertices change
  React.useEffect(() => {
    setPositions(prev => {
      const next = { ...prev };
      vertices.forEach((v, idx) => {
        if (!next[v.id]) {
          next[v.id] = {
            x: v.x || 100 + (idx % 4) * 200,
            y: v.y || 100 + Math.floor(idx / 4) * 120
          };
        }
      });
      return next;
    });
  }, [vertices]);

  const handleMouseDown = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setDraggingNode(id);
    if (onNodeSelect) onNodeSelect(id);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!draggingNode || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    const x = Math.max(40, Math.min(rect.width - 40, e.clientX - rect.left));
    const y = Math.max(40, Math.min(rect.height - 40, e.clientY - rect.top));
    setPositions(prev => ({
      ...prev,
      [draggingNode]: { x, y }
    }));
  };

  const handleMouseUp = () => {
    setDraggingNode(null);
  };

  // Helper to test if an edge is highlighted
  const isEdgeHighlighted = (u: string, v: string) => {
    return highlightedEdges.some(
      he => (he.source === u && he.target === v) || (he.source === v && he.target === u)
    );
  };

  // Helper to check if edge is part of highlightPath sequence
  const isPathEdge = (u: string, v: string) => {
    if (highlightPath.length < 2) return false;
    for (let i = 0; i < highlightPath.length - 1; i++) {
      const p1 = highlightPath[i];
      const p2 = highlightPath[i + 1];
      if ((p1 === u && p2 === v) || (p1 === v && p2 === u)) return true;
    }
    return false;
  };

  const getNodeColor = (tier?: string) => {
    switch (tier) {
      case 'Core':
        return { bg: '#2563EB', ring: '#1D4ED8', text: '#FFFFFF', badge: 'bg-blue-600' };
      case 'Distribution':
        return { bg: '#0D9488', ring: '#0F766E', text: '#FFFFFF', badge: 'bg-teal-600' };
      default:
        return { bg: '#475569', ring: '#334155', text: '#FFFFFF', badge: 'bg-slate-600' };
    }
  };

  const handleResetPositions = () => {
    const pos: Record<string, { x: number; y: number }> = {};
    vertices.forEach((v, idx) => {
      pos[v.id] = {
        x: v.x || 100 + (idx % 4) * 200,
        y: v.y || 100 + Math.floor(idx / 4) * 120
      };
    });
    setPositions(pos);
  };

  return (
    <div className="relative bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-inner select-none">
      {/* Canvas Top Bar */}
      <div className="absolute top-3 left-3 z-10 flex items-center space-x-2">
        <span className="text-[11px] font-medium bg-slate-800/90 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700 backdrop-blur">
          Interactive Topology Graph • {vertices.length} Nodes • {edges.length} Links
        </span>
      </div>

      <div className="absolute top-3 right-3 z-10 flex items-center space-x-2">
        <button
          onClick={handleResetPositions}
          title="Reset Node Coordinates"
          className="text-xs bg-slate-800/90 hover:bg-slate-700 text-slate-300 p-1.5 rounded-lg border border-slate-700 transition"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* SVG Rendering Surface */}
      <svg
        ref={svgRef}
        className="w-full cursor-crosshair"
        style={{ height }}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      >
        <defs>
          <radialGradient id="grid-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#1E293B" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#0F172A" stopOpacity="1" />
          </radialGradient>
        </defs>

        <rect width="100%" height="100%" fill="url(#grid-glow)" />

        {/* Draw Edges */}
        {edges.map((e, idx) => {
          const p1 = positions[e.source];
          const p2 = positions[e.target];
          if (!p1 || !p2) return null;

          const isHighlighted = isEdgeHighlighted(e.source, e.target);
          const isPath = isPathEdge(e.source, e.target);

          const midX = (p1.x + p2.x) / 2;
          const midY = (p1.y + p2.y) / 2;

          let strokeColor = '#334155';
          let strokeWidth = 1.5;
          let strokeDash = 'none';

          if (isPath) {
            strokeColor = '#F59E0B'; // Amber path
            strokeWidth = 3.5;
          } else if (isHighlighted) {
            strokeColor = '#10B981'; // Green/Emerald MST
            strokeWidth = 3.0;
          }

          return (
            <g key={`edge-${idx}`}>
              <line
                x1={p1.x}
                y1={p1.y}
                x2={p2.x}
                y2={p2.y}
                stroke={strokeColor}
                strokeWidth={strokeWidth}
                strokeDasharray={strokeDash}
                strokeLinecap="round"
                className="transition-colors duration-200"
              />
              {/* Edge Weight Pill Badge */}
              <rect
                x={midX - 18}
                y={midY - 9}
                width={36}
                height={18}
                rx={4}
                fill="#0F172A"
                stroke={isHighlighted || isPath ? strokeColor : '#475569'}
                strokeWidth={1}
              />
              <text
                x={midX}
                y={midY + 3.5}
                textAnchor="middle"
                fill={isHighlighted || isPath ? '#F8FAFC' : '#94A3B8'}
                fontSize="10"
                fontFamily="JetBrains Mono"
                fontWeight="bold"
              >
                {e.weight}
              </text>
            </g>
          );
        })}

        {/* Draw Vertices */}
        {vertices.map((v) => {
          const p = positions[v.id] || { x: 100, y: 100 };
          const colors = getNodeColor(v.tier);
          const isSelected = selectedNodeId === v.id;
          const isDragging = draggingNode === v.id;

          return (
            <g
              key={`vertex-${v.id}`}
              transform={`translate(${p.x}, ${p.y})`}
              onMouseDown={(e) => handleMouseDown(v.id, e)}
              className="cursor-grab active:cursor-grabbing"
            >
              {/* Pulse Ring if Selected */}
              {isSelected && (
                <circle
                  r={26}
                  fill="none"
                  stroke="#38BDF8"
                  strokeWidth={2}
                  strokeDasharray="4 2"
                  className="animate-spin"
                />
              )}

              {/* Main Node Circle */}
              <circle
                r={20}
                fill={colors.bg}
                stroke={isSelected ? '#38BDF8' : colors.ring}
                strokeWidth={isDragging ? 3 : 2}
                className="shadow-md transition-all duration-150"
              />

              {/* Node ID Label */}
              <text
                textAnchor="middle"
                dy="4"
                fill={colors.text}
                fontSize="10"
                fontFamily="Inter"
                fontWeight="bold"
              >
                {v.id.length > 7 ? v.id.substring(0, 6) : v.id}
              </text>

              {/* Sub-label Below Node */}
              <text
                textAnchor="middle"
                dy="32"
                fill="#CBD5E1"
                fontSize="11"
                fontFamily="Inter"
                fontWeight="500"
              >
                {v.label}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend Footer */}
      <div className="bg-slate-950/80 px-4 py-2 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center space-x-4">
          <span className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-600 inline-block"></span>
            <span>Core Tier</span>
          </span>
          <span className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-teal-600 inline-block"></span>
            <span>Distribution Tier</span>
          </span>
          <span className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-slate-500 inline-block"></span>
            <span>Access Tier</span>
          </span>
          {highlightedEdges.length > 0 && (
            <span className="flex items-center space-x-1.5 font-semibold text-emerald-400">
              <span className="w-4 h-1 bg-emerald-500 rounded inline-block"></span>
              <span>MST Selected Links</span>
            </span>
          )}
          {highlightPath.length > 0 && (
            <span className="flex items-center space-x-1.5 font-semibold text-amber-400">
              <span className="w-4 h-1 bg-amber-500 rounded inline-block"></span>
              <span>Active Tour/Path</span>
            </span>
          )}
        </div>
        <span className="text-[11px] text-slate-500 flex items-center">
          <Move className="w-3 h-3 mr-1" /> Click & drag nodes to reorganize topology
        </span>
      </div>
    </div>
  );
};
