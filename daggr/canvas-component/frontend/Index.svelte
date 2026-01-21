<script lang="ts">
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import { Gradio } from "@gradio/utils";

	/* ============================================
	 * CHATBOT IMPORTS - COMMENTED OUT
	 * ============================================
	// import ChatBot from "./shared/ChatBot.svelte";
	// import { BlockLabel } from "@gradio/atoms";
	// import { Chat } from "@gradio/icons";
	// import type { Message, ExampleMessage, NormalisedMessage } from "./types";
	// import type { ChatbotProps, ChatbotEvents } from "./types";
	// import { normalise_messages } from "./shared/utils";
	*/

	// Canvas-specific types
	interface CanvasData {
		name: string;
		nodes: any[];
		edges: any[];
	}

	interface CanvasEvents {
		change: CanvasData;
	}

	interface CanvasProps {
		value: CanvasData;
		height: number | string | undefined;
	}

	let props = $props();
	const gradio = new Gradio<CanvasEvents, CanvasProps>(props);

	// Canvas state
	let canvasRef: HTMLDivElement;
	let transform = $state({ x: 50, y: 50, scale: 1 });
	let isPanning = $state(false);
	let startPan = $state({ x: 0, y: 0 });

	// Get graph name from value
	let graphName = $derived(gradio.props.value?.name || "daggr workflow");

	function handleMouseDown(e: MouseEvent) {
		if (e.button === 0) {
			isPanning = true;
			startPan = { x: e.clientX - transform.x, y: e.clientY - transform.y };
		}
	}

	function handleMouseMove(e: MouseEvent) {
		if (isPanning) {
			transform.x = e.clientX - startPan.x;
			transform.y = e.clientY - startPan.y;
		}
	}

	function handleMouseUp() {
		isPanning = false;
	}

	function handleWheel(e: WheelEvent) {
		e.preventDefault();
		const delta = e.deltaY > 0 ? 0.9 : 1.1;
		const newScale = Math.max(0.1, Math.min(3, transform.scale * delta));
		transform.scale = newScale;
	}

	/* ============================================
	 * CHATBOT DERIVED STATE - COMMENTED OUT
	 * ============================================
	// let _value: NormalisedMessage[] | null = $derived(
	// 	normalise_messages(gradio.props.value as Message[], gradio.shared.root)
	// );
	//
	// let show_progress = $derived.by(() => {
	// 	if (gradio.shared.loading_status.status === "error") {
	// 		return "full";
	// 	}
	// 	return gradio.shared.loading_status.show_progress === "hidden"
	// 		? "hidden"
	// 		: "minimal";
	// });
	*/
</script>

<Block
	elem_id={gradio.shared.elem_id}
	elem_classes={gradio.shared.elem_classes}
	visible={gradio.shared.visible}
	padding={false}
	scale={gradio.shared.scale}
	min_width={gradio.shared.min_width}
	height={gradio.props.height || "100vh"}
	allow_overflow={false}
	flex={true}
>
	{#if gradio.shared.loading_status}
		<StatusTracker
			autoscroll={gradio.shared.autoscroll}
			i18n={gradio.i18n}
			{...gradio.shared.loading_status}
			on_clear_status={() =>
				gradio.dispatch("clear_status", gradio.shared.loading_status)}
		/>
	{/if}

	<!-- Canvas Container -->
	<div 
		class="canvas-container"
		bind:this={canvasRef}
		onmousedown={handleMouseDown}
		onmousemove={handleMouseMove}
		onmouseup={handleMouseUp}
		onmouseleave={handleMouseUp}
		onwheel={handleWheel}
	>
		<!-- Infinite Canvas -->
		<div 
			class="canvas"
			style="transform: translate({transform.x}px, {transform.y}px) scale({transform.scale})"
		>
			<!-- Graph Title -->
			<div class="graph-title">
				<span class="title-icon">◆</span>
				{graphName}
			</div>

			<!-- Placeholder for nodes - to be implemented -->
			<div class="placeholder-text">
				Canvas ready. Nodes will appear here.
			</div>
		</div>

		<!-- Grid Background (stays fixed) -->
		<svg class="grid-background">
			<defs>
				<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
					<circle cx="20" cy="20" r="1" fill="rgba(249, 115, 22, 0.15)" />
				</pattern>
			</defs>
			<rect width="100%" height="100%" fill="url(#grid)" />
		</svg>
	</div>

	<!-- ============================================
	     CHATBOT COMPONENT - COMMENTED OUT
	     ============================================
	{#if gradio.shared.show_label}
		<BlockLabel
			show_label={gradio.shared.show_label}
			Icon={Chat}
			float={true}
			label={gradio.shared.label || "Chatbot"}
		/>
	{/if}
	<ChatBot ... all props ... />
	-->
</Block>

<style>
	.canvas-container {
		position: relative;
		width: 100%;
		height: 100%;
		overflow: hidden;
		background: linear-gradient(165deg, #0a0a0a 0%, #111 50%, #0a0a0a 100%);
		cursor: grab;
	}

	.canvas-container:active {
		cursor: grabbing;
	}

	.grid-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 0;
	}

	.canvas {
		position: absolute;
		top: 0;
		left: 0;
		transform-origin: 0 0;
		z-index: 1;
	}

	.graph-title {
		position: absolute;
		top: 20px;
		left: 20px;
		font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
		font-size: 28px;
		font-weight: 700;
		color: #fff;
		display: flex;
		align-items: center;
		gap: 12px;
		text-shadow: 0 2px 20px rgba(249, 115, 22, 0.3);
	}

	.title-icon {
		color: #f97316;
		font-size: 24px;
	}

	.placeholder-text {
		position: absolute;
		top: 80px;
		left: 20px;
		font-family: 'JetBrains Mono', monospace;
		font-size: 14px;
		color: rgba(255, 255, 255, 0.4);
	}

	/* ============================================
	 * CHATBOT STYLES - COMMENTED OUT
	 * ============================================
	.wrapper {
		display: flex;
		position: relative;
		flex-direction: column;
		align-items: start;
		width: 100%;
		height: 100%;
		flex-grow: 1;
	}

	:global(.progress-text) {
		right: auto;
	}
	*/
</style>
