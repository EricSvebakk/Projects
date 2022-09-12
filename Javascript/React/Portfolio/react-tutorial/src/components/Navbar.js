
import React, { Component } from 'react'
// import logo from 'logo.svg'

import './Components.css'

class MyNavbar extends Component {
	
	render() {
		return (
			<nav>
				<ul id="primary-nagivation" className="primary-navigation-flex">
					<li class="active">
						<a href="index.html">
							<span aria-hidden="true">00</span>Home
						</a>
					</li>
					<li>
						<a>
							<span aria-hidden="true">01</span>Something
						</a>
					</li>
					<li>
						<a>
							<span aria-hidden="true">02</span>Other
						</a>
					</li>
				</ul>
			</nav>
		)
	}
}

export default MyNavbar;