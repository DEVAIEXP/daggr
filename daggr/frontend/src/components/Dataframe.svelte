<script lang="ts">
	interface DataframeValue {
		headers: string[];
		data: (string | number | boolean | null)[][];
	}

	interface Props {
		label: string;
		value: DataframeValue | null;
		editable?: boolean;
		maxHeight?: number;
		wrap?: boolean;
		onchange?: (value: DataframeValue) => void;
	}

	let { 
		label, 
		value, 
		editable = false, 
		maxHeight = 300,
		wrap = true,
		onchange 
	}: Props = $props();

	let editingCell: { row: number; col: number } | null = $state(null);
	let editValue = $state('');

	function startEdit(row: number, col: number, currentValue: any) {
		if (!editable) return;
		editingCell = { row, col };
		editValue = String(currentValue ?? '');
	}

	function commitEdit() {
		if (!editingCell || !value) return;
		const { row, col } = editingCell;
		const newData = value.data.map((r, ri) => 
			ri === row ? r.map((c, ci) => ci === col ? editValue : c) : r
		);
		onchange?.({ ...value, data: newData });
		editingCell = null;
	}

	function cancelEdit() {
		editingCell = null;
	}

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			commitEdit();
		} else if (e.key === 'Escape') {
			cancelEdit();
		}
	}

	function copyTable() {
		if (!value) return;
		const text = [
			value.headers.join('\t'),
			...value.data.map(row => row.map(c => c ?? '').join('\t'))
		].join('\n');
		navigator.clipboard.writeText(text);
	}
</script>

<div class="gr-dataframe-wrap">
	<div class="gr-header">
		<span class="gr-label">{label}</span>
		<div class="table-actions">
			{#if value}
				<button class="action-btn" onclick={copyTable} title="Copy to clipboard">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
						<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
					</svg>
				</button>
			{/if}
		</div>
	</div>

	{#if value && value.data.length > 0}
		<div class="table-container" style:max-height="{maxHeight}px">
			<table class:wrap>
				<thead>
					<tr>
						<th class="row-num">#</th>
						{#each value.headers as header}
							<th>{header}</th>
						{/each}
					</tr>
				</thead>
				<tbody>
					{#each value.data as row, ri}
						<tr>
							<td class="row-num">{ri + 1}</td>
							{#each row as cell, ci}
								<td 
									class:editable
									ondblclick={() => startEdit(ri, ci, cell)}
								>
									{#if editingCell?.row === ri && editingCell?.col === ci}
										<input
											type="text"
											class="cell-edit"
											bind:value={editValue}
											onblur={commitEdit}
											onkeydown={handleKeyDown}
										/>
									{:else}
										<span class="cell-content">{cell ?? ''}</span>
									{/if}
								</td>
							{/each}
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<div class="table-footer">
			<span>{value.data.length} rows × {value.headers.length} columns</span>
		</div>
	{:else}
		<div class="gr-empty">No data</div>
	{/if}
</div>

<style>
	.gr-dataframe-wrap {
		background: #1a1a1a;
		border: 1px solid #333;
		border-radius: 6px;
		overflow: hidden;
	}

	.gr-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 6px;
	}

	.gr-label {
		font-size: 10px;
		font-weight: 400;
		color: #888;
		padding-left: 4px;
	}

	.table-actions {
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

	.table-container {
		overflow: auto;
		margin: 0 6px;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 11px;
	}

	table.wrap td {
		white-space: normal;
		word-break: break-word;
	}

	table:not(.wrap) td {
		white-space: nowrap;
	}

	th, td {
		padding: 4px 8px;
		text-align: left;
		border-bottom: 1px solid #2a2a2a;
	}

	th {
		background: #222;
		color: #888;
		font-weight: 500;
		font-size: 10px;
		position: sticky;
		top: 0;
		z-index: 1;
	}

	td {
		color: #e5e7eb;
	}

	td.editable {
		cursor: pointer;
	}

	td.editable:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.row-num {
		color: #555;
		width: 40px;
		text-align: center;
		font-size: 10px;
	}

	tbody tr:hover {
		background: rgba(255, 255, 255, 0.02);
	}

	.cell-content {
		display: block;
		max-width: 200px;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.cell-edit {
		width: 100%;
		padding: 2px 4px;
		font-size: 11px;
		color: #e5e7eb;
		background: #333;
		border: 1px solid #f97316;
		border-radius: 2px;
		outline: none;
	}

	.table-footer {
		padding: 4px 10px;
		font-size: 10px;
		color: #555;
		border-top: 1px solid #2a2a2a;
	}

	.gr-empty {
		font-size: 11px;
		color: #555;
		font-style: italic;
		padding: 6px;
		text-align: center;
	}
</style>

