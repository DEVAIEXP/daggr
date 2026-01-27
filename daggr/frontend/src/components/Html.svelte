<script lang="ts">
	interface Props {
		label?: string;
		value: string;
		showLabel?: boolean;
	}

	let { 
		label = '', 
		value, 
		showLabel = false
	}: Props = $props();
</script>

<div class="gr-html-wrap">
	{#if showLabel && label}
		<div class="gr-header">
			<span class="gr-label">{label}</span>
		</div>
	{/if}
	
	<div class="html-content">
		{@html value}
	</div>
</div>

<style>
	.gr-html-wrap {
		background: #1a1a1a;
		border: 1px solid #333;
		border-radius: 6px;
		overflow: hidden;
	}

	.gr-header {
		padding: 6px;
	}

	.gr-label {
		font-size: 10px;
		font-weight: 400;
		color: #888;
		padding-left: 4px;
	}

	.html-content {
		padding: 10px;
		font-size: 12px;
		line-height: 1.5;
		color: #e5e7eb;
	}
</style>

