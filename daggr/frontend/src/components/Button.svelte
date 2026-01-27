<script lang="ts">
	interface Props {
		value: string;
		variant?: 'primary' | 'secondary' | 'stop';
		size?: 'sm' | 'md' | 'lg';
		disabled?: boolean;
		onclick?: () => void;
	}

	let { 
		value, 
		variant = 'primary', 
		size = 'md', 
		disabled = false,
		onclick 
	}: Props = $props();
</script>

<button 
	class="gr-button {variant} {size}" 
	{disabled}
	onclick={() => onclick?.()}
>
	{value}
</button>

<style>
	.gr-button {
		font-family: inherit;
		font-weight: 500;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		transition: all 0.15s;
		display: inline-flex;
		align-items: center;
		justify-content: center;
	}

	.gr-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.sm {
		padding: 4px 10px;
		font-size: 10px;
	}

	.md {
		padding: 6px 14px;
		font-size: 11px;
	}

	.lg {
		padding: 8px 18px;
		font-size: 12px;
	}

	.primary {
		background: #f97316;
		color: white;
	}

	.primary:hover:not(:disabled) {
		background: #ea580c;
	}

	.primary:active:not(:disabled) {
		background: #c2410c;
	}

	.secondary {
		background: #2a2a2a;
		color: #e5e7eb;
		border: 1px solid #3a3a3a;
	}

	.secondary:hover:not(:disabled) {
		background: #333;
		border-color: #444;
	}

	.secondary:active:not(:disabled) {
		background: #3a3a3a;
	}

	.stop {
		background: #dc2626;
		color: white;
	}

	.stop:hover:not(:disabled) {
		background: #b91c1c;
	}

	.stop:active:not(:disabled) {
		background: #991b1b;
	}
</style>

