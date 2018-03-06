import React, { Component } from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import 'react-notifications/lib/notifications.css';
import {NotificationContainer, NotificationManager} from 'react-notifications';

import OIDC from './components/OIDC';
import Nav from './components/Nav';
import Client from './components/Client';

import { OpalAPI } from './utils/opal-api';

export default class App extends Component {
    constructor(props){
        super(props);
        let session = sessionStorage.getItem('session');
        if(session){
            session = JSON.parse(session);
        }
        const cfg = sessionStorage.getItem('config');
        this.state = {
            isAuthenticated: session? true: false,
            session: session,
            config: cfg
        };
        this.onSuccessLogin = this.onSuccessLogin.bind(this);
        this.onFailedLogin = this.onFailedLogin.bind(this);
        this.onSaveConfiguration = this.onSaveConfiguration.bind(this);

        this.logout = this.logout.bind(this);
    }

    onSaveConfiguration(cfg){
        console.log(cfg);
        this.setState({
            config: cfg
        });
        sessionStorage.setItem('config', cfg);
    }

    onSuccessLogin(u){
        sessionStorage.setItem('session', JSON.stringify(u));
        this.setState({
            isAuthenticated: true,
            session: u
        });
        console.log('login success');
        const cfg = JSON.parse(this.state.config);
        window.location = cfg.base_url;
    }

    onFailedLogin(m){
        sessionStorage.removeItem("session");
        this.setState({
            isAuthenticated: false,
            session: null
        });
        NotificationManager.error(m, '', 1000);
    }

    logout() {
        sessionStorage.removeItem("session");
        this.setState({
            isAuthenticated: false,
            session: null
        });
    }

    render() {
        if(this.state.isAuthenticated){
            return (
                <div className="container">
                    <Router >
                        <div>
                        <Route render={props => <Nav logout={this.logout} />} />
                        <Switch>
                            <Route exact path="/" render={props => (
                                <div className="App">
                                    <header className="App-header">
                                        <img src={logo} className="App-logo" alt="logo" />
                                        <h1 className="App-title">Welcome to React</h1>
                                    </header>
                                    <p className="App-intro">
                                        To get started, edit <code>src/App.js</code> and save to reload.
                                    </p>
                                </div>
                            )} />
                            <Route path="/client" render={props => <Client />} />
                        </Switch>
                        </div>
                    </Router>
                    <NotificationContainer />
                </div>
            );
        }else{
            return (
                <div className="container">
                    <Router >
                        <Route render={(props) => <OIDC  onSaveConfiguration={this.onSaveConfiguration}
                                            onFailedLogin={this.onFailedLogin}
                                            onSuccessLogin={this.onSuccessLogin} {...props}/>} />
                    </Router>
                    <NotificationContainer />
                </div>
            );
        }
    }
}
