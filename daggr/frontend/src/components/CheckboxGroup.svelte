<script lang="ts">
	interface Props {
		label: string;
		choices: [string, string | number][];
		value: (string | number)[];
		disabled?: boolean;
		onchange?: (value: (string | number)[]) => void;
	}

	let { label, choices, value, disabled = false, onchange }: Props = $props();

	function toggleChoice(internalValue: string | number) {
		if (disabled) return;
		let newValue: (string | number)[];
		if (value.includes(internalValue)) {
			newValue = value.filter(v => v !== internalValue);
		} else {
			newValue = [...value, internalValue];
		}
		onchange?.(newValue);
	}
</script>

<div class="gr-checkboxgroup-wrap">
	<span class="gr-label">{label}</span>
	<div class="choices">
		{#each choices as [displayValue, internalValue]}
			<label class="choice" class:disabled class:selected={value.includes(internalValue)}>
				<input
					type="checkbox"
					checked={value.includes(internalValue)}
					{disabled}
					onchange={() => toggleChoice(internalValue)}
				/>
				<span class="checkmark"></span>
				<span class="choice-label">{displayValue}</span>
			</label>
		{/each}
	</div>
</div>

<style>
	.gr-checkboxgroup-wrap {
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

	.checkmark {
		width: 12px;
		height: 12px;
		background: #222;
		border: 1px solid #444;
		border-radius: 2px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s;
		flex-shrink: 0;
	}

	.choice input:checked ~ .checkmark {
		background: #f97316;
		border-color: #f97316;
	}

	.checkmark::after {
		content: '';
		display: none;
		width: 3px;
		height: 6px;
		border: solid white;
		border-width: 0 1.5px 1.5px 0;
		transform: rotate(45deg);
		margin-bottom: 1px;
	}

	.choice input:checked ~ .checkmark::after {
		display: block;
	}

	.choice-label {
		font-size: 11px;
		color: #e5e7eb;
	}
</style>

