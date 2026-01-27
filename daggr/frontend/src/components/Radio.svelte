<script lang="ts">
	interface Props {
		label: string;
		choices: [string, string | number][];
		value: string | number | null;
		disabled?: boolean;
		onchange?: (value: string | number) => void;
	}

	let { label, choices, value, disabled = false, onchange }: Props = $props();

	function selectChoice(internalValue: string | number) {
		if (disabled) return;
		onchange?.(internalValue);
	}
</script>

<div class="gr-radio-wrap">
	<span class="gr-label">{label}</span>
	<div class="choices">
		{#each choices as [displayValue, internalValue]}
			<label class="choice" class:disabled class:selected={value === internalValue}>
				<input
					type="radio"
					checked={value === internalValue}
					{disabled}
					onchange={() => selectChoice(internalValue)}
				/>
				<span class="radio-mark"></span>
				<span class="choice-label">{displayValue}</span>
			</label>
		{/each}
	</div>
</div>

<style>
	.gr-radio-wrap {
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
		padding: 6px 10px 4px;
	}

	.choices {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		padding: 0 10px 8px;
	}

	.choice {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 4px 8px;
		background: #2a2a2a;
		border: 1px solid #3a3a3a;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.15s;
	}

	.choice:hover:not(.disabled) {
		border-color: #444;
		background: #333;
	}

	.choice.selected {
		background: rgba(249, 115, 22, 0.15);
		border-color: rgba(249, 115, 22, 0.4);
	}

	.choice.disabled {
		cursor: not-allowed;
		opacity: 0.6;
	}

	.choice input {
		position: absolute;
		opacity: 0;
		cursor: pointer;
		height: 0;
		width: 0;
	}

	.radio-mark {
		width: 12px;
		height: 12px;
		background: #222;
		border: 1px solid #444;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s;
		flex-shrink: 0;
	}

	.choice input:checked ~ .radio-mark {
		border-color: #f97316;
	}

	.radio-mark::after {
		content: '';
		display: none;
		width: 6px;
		height: 6px;
		background: #f97316;
		border-radius: 50%;
	}

	.choice input:checked ~ .radio-mark::after {
		display: block;
	}

	.choice-label {
		font-size: 11px;
		color: #e5e7eb;
	}
</style>

