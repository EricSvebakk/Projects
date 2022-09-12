
import React, { Component } from 'react'
import './Components.css'

class Counter extends Component {
	constructor(props) {
		super(props);
		this.state = {
			counter: 0,
			increment: 0.1
		};
	}
	
	componentDidMount() {
		this.counterID = setInterval(
			() => this.tick(),
			100
		);
	}
	
	componentWillUnmount() {
		clearInterval(this.counterID);
	}
	
	tick() {
		this.setState(
			(state) => (
				{counter: state.counter + state.increment}
			)
		);
	}
	
	render() {
		return (
			<div className='TimerComponent'>
				<p>TIMER: {this.state.counter.toFixed(1)}s</p>
			</div>
		);
	}
}

export default Counter