<script lang="ts">
	interface Props {
		label: string;
		value: string | null;
	}

	let { label, value }: Props = $props();

	let filename = $derived(value ? value.split('/').pop() || 'model.glb' : '');

	function downloadModel() {
		if (!value) return;
		const link = document.createElement('a');
		link.href = value;
		link.download = filename;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
</script>

<div class="gr-model3d-wrap">
	<div class="gr-header">
		<span class="gr-label">{label}</span>
		{#if value}
			<button class="download-btn" onclick={downloadModel} title="Download">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
					<polyline points="7 10 12 15 17 10"/>
					<line x1="12" y1="15" x2="12" y2="3"/>
				</svg>
			</button>
		{/if}
	</div>

	{#if value}
		<div class="previewer-container">
			<div class="tips-wrapper">
				<div class="tips-icon">💡 Tips</div>
				<div class="tips-text">3D preview not available. Click download to view in a 3D viewer.</div>
			</div>
			<div class="model-info">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="model-icon">
					<path d="M12 2L2 7l10 5 10-5-10-5z"/>
					<path d="M2 17l10 5 10-5"/>
					<path d="M2 12l10 5 10-5"/>
				</svg>
				<span class="model-name">{filename}</span>
			</div>
		</div>
	{:else}
		<div class="gr-empty">No model</div>
	{/if}
</div>

<style>
	.gr-model3d-wrap {
		background: #1a1a1a;
		border: 1px solid #333;
		border-radius: 6px;
		overflow: hidden;
	}

	.gr-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 6px 10px;
	}

	.gr-label {
		font-size: 10px;
		font-weight: 400;
		color: #888;
	}

	.download-btn {
		width: 20px;
		height: 20px;
		padding: 3px;
		border: none;
		background: rgba(255, 255, 255, 0.08);
		border-radius: 4px;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: background 0.15s;
	}

	.download-btn svg {
		width: 12px;
		height: 12px;
		color: #888;
	}

	.download-btn:hover {
		background: rgba(249, 115, 22, 0.3);
	}

	.download-btn:hover svg {
		color: #f97316;
	}

	.previewer-container {
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.tips-wrapper {
		display: flex;
		align-items: flex-start;
		gap: 6px;
		padding: 8px;
		background: rgba(249, 115, 22, 0.1);
		border-radius: 4px;
	}

	.tips-icon {
		font-size: 10px;
		flex-shrink: 0;
	}

	.tips-text {
		font-size: 10px;
		color: #9ca3af;
		line-height: 1.4;
	}

	.model-info {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 10px;
		background: #2a2a2a;
		border-radius: 4px;
	}

	.model-icon {
		width: 24px;
		height: 24px;
		color: #f97316;
		flex-shrink: 0;
	}

	.model-name {
		font-size: 11px;
		color: #e5e7eb;
		word-break: break-all;
	}

	.gr-empty {
		font-size: 11px;
		color: #555;
		font-style: italic;
		padding: 20px;
		text-align: center;
	}
</style>

