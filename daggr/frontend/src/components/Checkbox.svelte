<script lang="ts">
	interface Props {
		label: string;
		value: boolean;
		disabled?: boolean;
		onchange?: (value: boolean) => void;
	}

	let { label, value, disabled = false, onchange }: Props = $props();

	function handleChange(e: Event) {
		const target = e.target as HTMLInputElement;
		onchange?.(target.checked);
	}
</script>

<div class="gr-checkbox-wrap">
	<label class="checkbox-container" class:disabled>
		<input
			type="checkbox"
			checked={value}
			{disabled}
			onchange={handleChange}
		/>
		<span class="checkmark"></span>
		<span class="gr-label">{label}</span>
	</label>
</div>

<style>
	.gr-checkbox-wrap {
		background: #1a1a1a;
		border: 1px solid #333;
		border-radius: 6px;
		padding: 8px 10px;
	}

	.checkbox-container {
		display: flex;
		align-items: center;
		gap: 8px;
		cursor: pointer;
		position: relative;
	}

	.checkbox-container.disabled {
		cursor: not-allowed;
		opacity: 0.6;
	}

	.checkbox-container input {
		position: absolute;
		opacity: 0;
		cursor: pointer;
		height: 0;
		width: 0;
	}

	.checkmark {
		width: 14px;
		height: 14px;
		background: #2a2a2a;
		border: 1px solid #444;
		border-radius: 3px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s;
		flex-shrink: 0;
	}

	.checkbox-container:hover .checkmark {
		border-color: #555;
	}

	.checkbox-container input:checked ~ .checkmark {
		background: #f97316;
		border-color: #f97316;
	}

	.checkmark::after {
		content: '';
		display: none;
		width: 4px;
		height: 7px;
		border: solid white;
		border-width: 0 2px 2px 0;
		transform: rotate(45deg);
		margin-bottom: 2px;
	}

	.checkbox-container input:checked ~ .checkmark::after {
		display: block;
	}

	.checkbox-container:focus-within .checkmark {
		border-color: #f97316;
		box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2);
	}

	.gr-label {
		font-size: 11px;
		color: #e5e7eb;
	}

	.checkbox-container.disabled .gr-label {
		color: #666;
	}
</style>

