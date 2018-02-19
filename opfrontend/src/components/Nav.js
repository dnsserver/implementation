import React, {Component} from 'react';
import {Link} from 'react-router-dom';

export default class Nav extends Component {
    render(){
        return (
            <nav className="navbar navbar-default">
              <div className="container-fluid">
                <div className="navbar-header">
                  <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                    <span className="sr-only">Toggle navigation</span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                  </button>
                  <Link className="navbar-brand" to="/">OPAL-C</Link>
                </div>

                <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                  <ul className="nav navbar-nav">
                    <li><Link to="/client">Register Client</Link></li>
                    <li><Link to="/profile">Profile</Link></li>
                    <li><Link onClick={this.props.logout} to="/">Logout</Link></li>
                  </ul>
                </div>
              </div>
            </nav>
        );
    }
}
