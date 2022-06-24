
import React, { Component } from 'react'

// ===============================================================
const TableHeader = () => {
	return (
		<thead>
			<tr>
				<th>Index</th>
				<th>Name</th>
				<th>Job</th>
				<th>Delete</th>
			</tr>
		</thead>
	)
}

// ===============================================================
const TableBody = (props) => {
	
	// Maps input-argument to table-rows
	const rows = props.characterData.map(
		(row, index) => {
			
			return (
				<tr key={index}>
					<td>{index+1}</td>
					<td>{row.name}</td>
					<td>{row.job}</td>
					<td>
						<button onClick={() => props.removeCharacter(index)}>Delete</button>
					</td>
				</tr>
			)
			
		}
	)
	
	return <tbody>{rows}</tbody>
}

// ===============================================================
/**
 * Test-table made by Eric
 */
class Table extends Component {
	render() {
		
		const {characterData, removeCharacter} = this.props
		
		return (
			<table>
				<TableHeader />
				<TableBody characterData={characterData} removeCharacter={removeCharacter} />
			</table>
		)
	}
}

export default Table