/**
 * StegVerse Demo — Boundary Visualization
 * Renders the GCAT/BCAT geometric boundary, proposed state, and GOD divergence
 * in real-time using HTML5 Canvas.
 */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined'
        ? module.exports = factory()
        : typeof define === 'function' && define.amd
        ? define(factory)
        : (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.BoundaryViz = factory());
}(this, function () {
    'use strict';

    const COLORS = {
        boundary: '#4ade80',
        boundaryFill: 'rgba(74, 222, 128, 0.08)',
        centroid: '#ffffff',
        proposedAllow: '#4ade80',
        proposedDeny: '#fbbf24',
        proposedFail: '#f87171',
        godVector: '#60a5fa',
        grid: 'rgba(255,255,255,0.06)',
        text: '#94a3b8'
    };

    function init(canvasId, width, height) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return null;
        canvas.width = width || canvas.clientWidth * 2;
        canvas.height = height || canvas.clientHeight * 2;
        const ctx = canvas.getContext('2d');
        ctx.scale(2, 2);
        return { canvas, ctx, w: canvas.width / 2, h: canvas.height / 2 };
    }

    function project3d(point, rotationX, rotationY, scale, offsetX, offsetY) {
        const [x, y, z] = point;
        const cx = Math.cos(rotationX), sx = Math.sin(rotationX);
        const cy = Math.cos(rotationY), sy = Math.sin(rotationY);
        const x1 = x * cy + z * sy;
        const y1 = y * cx - (z * cy - x * sy) * sx;
        const z1 = y * sx + (z * cy - x * sy) * cx;
        return [
            offsetX + x1 * scale,
            offsetY - y1 * scale,
            z1
        ];
    }

    function drawGrid(viz, rotationX, rotationY, scale, offsetX, offsetY) {
        const { ctx, w, h } = viz;
        ctx.strokeStyle = COLORS.grid;
        ctx.lineWidth = 0.5;
        const steps = 6;
        const step = 1.0 / steps;
        for (let i = -steps; i <= steps; i++) {
            for (let j = -steps; j <= steps; j++) {
                const p1 = project3d([i * step, -1, j * step], rotationX, rotationY, scale, offsetX, offsetY);
                const p2 = project3d([i * step, 1, j * step], rotationX, rotationY, scale, offsetX, offsetY);
                ctx.beginPath();
                ctx.moveTo(p1[0], p1[1]);
                ctx.lineTo(p2[0], p2[1]);
                ctx.stroke();
            }
        }
    }

    function drawBoundary(viz, boundary, rotationX, rotationY, scale, offsetX, offsetY) {
        const { ctx } = viz;
        const c = project3d(boundary.centroid, rotationX, rotationY, scale, offsetX, offsetY);
        const r = boundary.radius * scale;

        // Draw boundary sphere (as circle for 2D projection)
        ctx.beginPath();
        ctx.arc(c[0], c[1], r, 0, Math.PI * 2);
        ctx.fillStyle = COLORS.boundaryFill;
        ctx.fill();
        ctx.strokeStyle = COLORS.boundary;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Draw centroid
        ctx.beginPath();
        ctx.arc(c[0], c[1], 3, 0, Math.PI * 2);
        ctx.fillStyle = COLORS.centroid;
        ctx.fill();

        // Label
        ctx.fillStyle = COLORS.text;
        ctx.font = '11px SF Mono, monospace';
        ctx.fillText('centroid', c[0] + 6, c[1] - 6);
    }

    function drawProposed(viz, proposed, boundary, rotationX, rotationY, scale, offsetX, offsetY) {
        const { ctx } = viz;
        const p = project3d(proposed, rotationX, rotationY, scale, offsetX, offsetY);
        const c = project3d(boundary.centroid, rotationX, rotationY, scale, offsetX, offsetY);

        // Determine color by verdict zone
        const god = GCATEvaluator.computeGOD(proposed, boundary);
        let color;
        if (god <= 1.0) color = COLORS.proposedAllow;
        else if (god <= 1.05) color = COLORS.proposedDeny;
        else color = COLORS.proposedFail;

        // Draw proposed point
        ctx.beginPath();
        ctx.arc(p[0], p[1], 5, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.stroke();

        // Draw GOD vector (line from centroid to proposed)
        ctx.beginPath();
        ctx.moveTo(c[0], c[1]);
        ctx.lineTo(p[0], p[1]);
        ctx.strokeStyle = COLORS.godVector;
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 3]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Label
        ctx.fillStyle = color;
        ctx.font = 'bold 11px SF Mono, monospace';
        ctx.fillText(`proposed (GOD=${god.toFixed(3)})`, p[0] + 8, p[1] - 8);
    }

    function drawCommitStates(viz, states, rotationX, rotationY, scale, offsetX, offsetY) {
        const { ctx } = viz;
        ctx.fillStyle = COLORS.boundary;
        states.forEach((s, i) => {
            const p = project3d(s, rotationX, rotationY, scale, offsetX, offsetY);
            ctx.beginPath();
            ctx.arc(p[0], p[1], 2, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.fillStyle = COLORS.text;
        ctx.font = '10px SF Mono, monospace';
        ctx.fillText(`${states.length} commit states`, 12, viz.h - 12);
    }

    function render(viz, inputs, result, rotationX, rotationY) {
        const { ctx, w, h } = viz;
        ctx.clearRect(0, 0, w, h);

        const scale = Math.min(w, h) * 0.35;
        const offsetX = w / 2;
        const offsetY = h / 2;

        drawGrid(viz, rotationX, rotationY, scale, offsetX, offsetY);
        drawBoundary(viz, result.boundary, rotationX, rotationY, scale, offsetX, offsetY);
        drawCommitStates(viz, inputs.commit_states, rotationX, rotationY, scale, offsetX, offsetY);
        drawProposed(viz, inputs.proposed_state, result.boundary, rotationX, rotationY, scale, offsetX, offsetY);

        // Legend
        ctx.fillStyle = COLORS.text;
        ctx.font = '10px sans-serif';
        ctx.fillText('← drag to rotate', 12, 20);
    }

    function attachInteractive(vizId, inputs, result) {
        const viz = init(vizId);
        if (!viz) return;

        let rotX = 0.3, rotY = 0.5;
        let dragging = false;
        let lastX, lastY;

        function draw() {
            render(viz, inputs, result, rotX, rotY);
        }

        viz.canvas.addEventListener('mousedown', e => {
            dragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
        });
        window.addEventListener('mousemove', e => {
            if (!dragging) return;
            rotY += (e.clientX - lastX) * 0.01;
            rotX += (e.clientY - lastY) * 0.01;
            lastX = e.clientX;
            lastY = e.clientY;
            draw();
        });
        window.addEventListener('mouseup', () => dragging = false);

        // Touch support
        viz.canvas.addEventListener('touchstart', e => {
            dragging = true;
            lastX = e.touches[0].clientX;
            lastY = e.touches[0].clientY;
        });
        viz.canvas.addEventListener('touchmove', e => {
            if (!dragging) return;
            e.preventDefault();
            rotY += (e.touches[0].clientX - lastX) * 0.01;
            rotX += (e.touches[0].clientY - lastY) * 0.01;
            lastX = e.touches[0].clientX;
            lastY = e.touches[0].clientY;
            draw();
        });
        viz.canvas.addEventListener('touchend', () => dragging = false);

        draw();
        return { draw, setRotation: (x, y) => { rotX = x; rotY = y; draw(); } };
    }

    return { init, render, attachInteractive };
}));
