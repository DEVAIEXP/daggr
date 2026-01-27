<script lang="ts">
	interface Props {
		label: string;
		value: string;
		disabled?: boolean;
		onchange?: (value: string) => void;
	}

	let { label, value, disabled = false, onchange }: Props = $props();

	let inputEl: HTMLInputElement | null = $state(null);

	function handleChange(e: Event) {
		const target = e.target as HTMLInputElement;
		onchange?.(target.value);
	}

	function handleTextInput(e: Event) {
		const target = e.target as HTMLInputElement;
		let val = target.value;
		if (!val.startsWith('#')) val = '#' + val;
		if (/^#[0-9A-Fa-f]{6}$/.test(val)) {
			onchange?.(val);
		}
	}

	function openPicker() {
		inputEl?.click();
	}
</script>

<div class="gr-colorpicker-wrap">
	<span class="gr-label">{label}</span>
	<div class="picker-container">
		<input
			bind:this={inputEl}
			type="color"
			class="color-input"
			{value}
			{disabled}
			onchange={handleChange}
		/>
		<button 
			class="color-preview" 
			style:background-color={value}
			onclick={openPicker}
			{disabled}
		></button>
		<input
			type="text"
			class="hex-input"
			value={value.toUpperCase()}
			{disabled}
			oninput={handleTextInput}
		/>
	</div>
</div>

<style>
	.gr-colorpicker-wrap {
		background: #1a1a1a;
		border: 1px solid #333;
		border-radius: 6px;
		overflow: hidden;
	}

	.gr-label {
		display: block;
		font-size: 10px;
		font-weight: 400;
		color: #888;
		padding: 6px 10px 0;
	}

	.picker-container {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 10px 8px;
	}

	.color-input {
		position: absolute;
		width: 0;
		height: 0;
		opacity: 0;
		pointer-events: none;
	}

	.color-preview {
		width: 28px;
		height: 28px;
		border: 2px solid #3a3a3a;
		border-radius: 4px;
		cursor: pointer;
		transition: border-color 0.15s;
		flex-shrink: 0;
	}

	.color-preview:hover:not(:disabled) {
		border-color: #555;
	}

	.color-preview:disabled {
		cursor: not-allowed;
		opacity: 0.6;
	}

	.hex-input {
		flex: 1;
		min-width: 0;
		padding: 6px 8px;
		font-size: 11px;
		font-family: 'SF Mono', Monaco, monospace;
		color: #e5e7eb;
		background: #2a2a2a;
		border: 1px solid #3a3a3a;
		border-radius: 4px;
		outline: none;
	}

	.hex-input:focus {
		border-color: #f97316;
	}

	.hex-input:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
</style>

