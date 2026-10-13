import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { MetricsCard } from '../components/MetricsCard';
import { ExplanationCard } from '../components/ExplanationCard';
import { NetworkGraph } from '../components/NetworkGraph';
import { Server } from 'lucide-react';
import { AlgorithmExplanation } from '../types';

describe('MetricsCard Component', () => {
  it('renders title, value and subtitle properly', () => {
    render(
      <MetricsCard
        title="Test Metric"
        value="42 Units"
        subtitle="Test Subtitle"
        icon={Server}
        color="blue"
      />
    );
    expect(screen.getByText('Test Metric')).toBeInTheDocument();
    expect(screen.getByText('42 Units')).toBeInTheDocument();
    expect(screen.getByText('Test Subtitle')).toBeInTheDocument();
  });
});

describe('ExplanationCard Component', () => {
  const sampleExplanation: AlgorithmExplanation = {
    module_name: 'Module 1: Network Design & MST',
    real_world_question: 'How to connect nodes with minimum cost?',
    mathematical_formulation: 'min sum w(e)',
    input_properties: { vertices: 4 },
    selected_algorithm: "Prim's Algorithm",
    alternative_considered: "Kruskal's Algorithm",
    selection_reason: 'Higher density input',
    expected_time_complexity: 'O(E log V)',
    expected_space_complexity: 'O(V + E)',
    correctness_assumptions: 'Connected graph',
    actual_result_summary: 'Spanning tree generated',
    limitations_and_warnings: 'Cannot handle disconnected graph as full MST'
  };

  it('renders module name and decision details', () => {
    render(<ExplanationCard explanation={sampleExplanation} />);
    expect(screen.getByText('Module 1: Network Design & MST')).toBeInTheDocument();
    expect(screen.getByText("Prim's Algorithm")).toBeInTheDocument();
    expect(screen.getByText("Kruskal's Algorithm")).toBeInTheDocument();
    expect(screen.getByText('Higher density input')).toBeInTheDocument();
  });
});

describe('NetworkGraph Component', () => {
  it('renders svg elements for vertices and edges', () => {
    const vertices = [
      { id: 'N1', label: 'Node 1', tier: 'Core', x: 100, y: 100 },
      { id: 'N2', label: 'Node 2', tier: 'Access', x: 200, y: 200 }
    ];
    const edges = [
      { source: 'N1', target: 'N2', weight: 15.5 }
    ];

    const { container } = render(
      <NetworkGraph vertices={vertices} edges={edges} />
    );
    expect(container.querySelector('svg')).toBeInTheDocument();
    expect(screen.getByText('N1')).toBeInTheDocument();
    expect(screen.getByText('N2')).toBeInTheDocument();
    expect(screen.getByText('15.5')).toBeInTheDocument();
  });
});
