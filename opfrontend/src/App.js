import React, { Component } from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import 'react-notifications/lib/notifications.css';
import {NotificationContainer, NotificationManager} from 'react-notifications';

import OIDC from './components/OIDC';

import { OpalAPI } from './utils/opal-api';

export default class App extends Component {
    constructor(props){
        super(props);
        const token = sessionStorage.getItem('session');
        const cfg = sessionStorage.getItem('config');
        this.state = {
            isAuthenticated: token? true: false,
            auth_token: token,
            config: cfg
        };
        this.onSuccessLogin = this.onSuccessLogin.bind(this);
        this.onFailedLogin = this.onFailedLogin.bind(this);
        this.onSaveConfiguration = this.onSaveConfiguration.bind(this);
    }

    onSaveConfiguration(cfg){
        console.log(cfg);
        this.setState({
            config: cfg
        });
        sessionStorage.setItem('config', cfg);
    }

    onSuccessLogin(u){
        sessionStorage.setItem('session', u);
        this.setState({
            isAuthenticated: true,
            auth_token: u
        });
        NotificationManager.info('Welcome back!', '', 1000);
    }

    onFailedLogin(m){
        sessionStorage.clear();
        this.setState({
            isAuthenticated: false,
            auth_token: ''
        });
        NotificationManager.error(m, '', 1000);
    }

    render() {
        if(this.state.isAuthenticated){
            return (
                <div className="App">
                    <header className="App-header">
                        <img src={logo} className="App-logo" alt="logo" />
                        <h1 className="App-title">Welcome to React</h1>
                    </header>
                    <p className="App-intro">
                        To get started, edit <code>src/App.js</code> and save to reload.
                    </p>
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
