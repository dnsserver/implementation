import React, { Component } from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import 'react-notifications/lib/notifications.css';
import {NotificationContainer, NotificationManager} from 'react-notifications';

import OIDC from './components/OIDC';
import Nav from './components/Nav';
import Persona from './components/Persona';
import Profile from './components/Profile';
import OpalClient from './components/OpalClient';

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
            config: cfg,
            isAdmin: false
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
            session: u,
            isAdmin: false
        });
        const cfg = JSON.parse(this.state.config);
        window.location = cfg.base_url;
    }

    onFailedLogin(m){
        sessionStorage.removeItem("session");
        this.setState({
            isAuthenticated: false,
            session: null,
            isAdmin: false
        });
        NotificationManager.error(m, '', 1000);
    }

    logout() {
        sessionStorage.removeItem("session");
        this.setState({
            isAuthenticated: false,
            session: null,
            isAdmin: false
        });
    }

    componentDidMount() {
        if(!this.state.isAuthenticated){
            return;
        }
        let opalAPI = new OpalAPI();
        const config = JSON.parse(this.state.config);
        opalAPI.getUserInfo(config.userinfo_uri, this.state.session.access_token).then((data)=>{
            if(data['preferred_username'] === 'admin'){
                this.setState({
                    isAdmin: true
                });
            }else{
                this.setState({
                    isAdmin: false
                });
            }
        });
    }

    render() {
        if(this.state.isAuthenticated){
            return (
                <div className="container">
                    <Router >
                        <div>
                        <Route render={props => <Nav logout={this.logout} isAdmin={this.state.isAdmin}/>} />
                        <Switch>
                            <Route exact path="/" render={props => (
                                <div className="App">
                                    <header className="App-header">
                                        <img src={logo} className="App-logo" alt="logo" />
                                        <h1 className="App-title">Welcome to Oapl Client - React</h1>
                                    </header>
                                </div>
                            )} />
                            <Route path="/persona" render={props => <Persona isAdmin={this.state.isAdmin}/>} />
                            <Route path="/profile" render={props => <Profile />} />
                            <Route path="/opal_oidc/:id" render={props => <OpalClient {...props}/>} />
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
