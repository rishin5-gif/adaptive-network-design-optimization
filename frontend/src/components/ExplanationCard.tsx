import React, { useState } from 'react';
import { AlgorithmExplanation } from '../types';
import { BookOpen, Cpu, Info, AlertTriangle, CheckCircle, ChevronDown, ChevronUp } from 'lucide-react';

interface Props {
  explanation?: AlgorithmExplanation | null;
}

export const ExplanationCard: React.FC<Props> = ({ explanation }) => {
  const [expanded, setExpanded] = useState(false);

  if (!explanation) return null;

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden mb-6">
      <div className="bg-slate-900 px-5 py-4 text-white flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <span className="p-2 bg-blue-600/30 text-blue-400 rounded-lg">
            <Cpu className="w-5 h-5" />
          </span>
          <div>
            <span className="text-xs font-semibold tracking-wider text-blue-400 uppercase">
              Integrated Decision & Explanation Engine
            </span>
            <h3 className="text-base font-bold text-white">{explanation.module_name}</h3>
          </div>
        </div>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition-colors"
        >
          <span>{expanded ? 'Hide Technical Invariants' : 'View Full DAA Analysis'}</span>
          {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>
      </div>

      <div className="p-5 space-y-4">
        {/* Core Decision Summary */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50/60 border border-blue-100 rounded-lg p-3.5">
            <div className="text-xs font-semibold text-blue-800 uppercase tracking-wide mb-1 flex items-center">
              <CheckCircle className="w-3.5 h-3.5 mr-1.5 text-blue-600" />
              Selected Algorithm
            </div>
            <div className="text-sm font-bold text-blue-950">{explanation.selected_algorithm}</div>
            <div className="text-xs text-blue-700 mt-1">{explanation.selection_reason}</div>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3.5">
            <div className="text-xs font-semibold text-slate-600 uppercase tracking-wide mb-1 flex items-center">
              <Info className="w-3.5 h-3.5 mr-1.5 text-slate-500" />
              Alternative Considered
            </div>
            <div className="text-sm font-semibold text-slate-900">{explanation.alternative_considered}</div>
            <div className="flex items-center space-x-3 mt-2 text-xs">
              <span className="bg-slate-200 text-slate-700 px-2 py-0.5 rounded font-mono font-medium">
                Time: {explanation.expected_time_complexity}
              </span>
              <span className="bg-slate-200 text-slate-700 px-2 py-0.5 rounded font-mono font-medium">
                Space: {explanation.expected_space_complexity}
              </span>
            </div>
          </div>
        </div>

        {/* Real World Problem & Mathematical Abstraction */}
        <div className="space-y-2 text-xs text-slate-700">
          <div>
            <span className="font-semibold text-slate-900">Real-World Objective: </span>
            {explanation.real_world_question}
          </div>
          <div className="bg-slate-100/70 p-2.5 rounded font-mono text-slate-800 border border-slate-200/60">
            <span className="font-sans font-semibold text-slate-900">Mathematical Formulation: </span>
            {explanation.mathematical_formulation}
          </div>
        </div>

        {/* Expandable Technical Details */}
        {expanded && (
          <div className="pt-3 border-t border-slate-100 space-y-3 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="font-semibold text-slate-900 block mb-1">Correctness & Invariant Assumptions:</span>
                <p className="text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded border border-slate-100">
                  {explanation.correctness_assumptions}
                </p>
              </div>
              <div>
                <span className="font-semibold text-slate-900 block mb-1">Execution Summary:</span>
                <p className="text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded border border-slate-100">
                  {explanation.actual_result_summary}
                </p>
              </div>
            </div>

            <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3 rounded-lg flex items-start space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-amber-950">Limitations & Scalability Warnings: </span>
                <span className="text-amber-800">{explanation.limitations_and_warnings}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
