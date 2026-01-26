<script lang="ts">
	interface Props {
		label: string;
		value: any;
	}

	let { label, value }: Props = $props();

	let imgEl: HTMLImageElement | null = $state(null);

	let src = $derived.by(() => {
		if (!value) return null;
		if (typeof value === 'string') return value;
		if (value.url) return value.url;
		return null;
	});

	function downloadImage() {
		if (!src) return;
		const link = document.createElement('a');
		link.href = src;
		link.download = label || 'image';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	function openFullscreen() {
		if (!imgEl) return;
		if (imgEl.requestFullscreen) {
			imgEl.requestFullscreen();
		} else if ((imgEl as any).webkitRequestFullscreen) {
			(imgEl as any).webkitRequestFullscreen();
		} else if ((imgEl as any).msRequestFullscreen) {
			(imgEl as any).msRequestFullscreen();
		}
	}
</script>

<div class="gr-image-wrap">
	<div class="gr-header">
		<span class="gr-label">{label}</span>
		{#if src}
			<div class="image-actions">
				<button class="action-btn" onclick={openFullscreen} title="View fullscreen">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
					</svg>
				</button>
				<button class="action-btn" onclick={downloadImage} title="Download">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
						<polyline points="7 10 12 15 17 10"/>
						<line x1="12" y1="15" x2="12" y2="3"/>
					</svg>
				</button>
			</div>
		{/if}
	</div>
	{#if src}
		<div class="image-container">
			<img bind:this={imgEl} class="gr-image" {src} alt={label} />
		</div>
	{:else}
		<div class="gr-empty">No image</div>
	{/if}
</div>

<style>
	.gr-image-wrap {
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

	.image-actions {
		display: flex;
		gap: 4px;
	}

	.action-btn {
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

	.action-btn svg {
		width: 12px;
		height: 12px;
		color: #888;
	}

	.action-btn:hover {
		background: rgba(255, 255, 255, 0.15);
	}

	.action-btn:hover svg {
		color: #fff;
	}

	.image-container {
		padding: 0 10px 10px;
	}

	.gr-image {
		width: 100%;
		max-height: 80px;
		object-fit: contain;
		display: block;
		border-radius: 4px;
	}

	.gr-empty {
		font-size: 11px;
		color: #555;
		font-style: italic;
		padding: 10px;
		text-align: center;
	}
</style>
