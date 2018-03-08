import React, { Component } from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import 'react-notifications/lib/notifications.css';

import {NotificationContainer} from 'react-notifications';

import Nav from './components/Nav';
import Persona from './components/Persona';
import Profile from './components/Profile';
import OpalClient from './components/OpalClient';

import { OpalAPI } from './utils/opal-api';

export default class App extends Component {
    constructor(props){
        super(props);
        this.state = {
            isAuthenticated: false,
            isAdmin: false,
            username: null
        };
        this.logout = this.logout.bind(this);
    }

    logout() {
        const opalAPI = new OpalAPI();
        this.setState({
            isAuthenticated: false,
            isAdmin: false,
            username: null
        });
        opalAPI.logout().then((data)=>{
            window.location = '/';
        });
    }

    componentDidMount() {
        const opalAPI = new OpalAPI();
        opalAPI.getTokenInfo().then((data)=>{
            let auth = false;
            let admin = false;
            let username = null;
            if(data['user_id']){
                auth = true;
                if(data['user_id']==='admin'){
                    admin = true;
                }
                username = data['user_id'];
            }
            this.setState({
                isAuthenticated: auth,
                isAdmin: admin,
                username: username
            });
            opalAPI.getConfiguration().then((data)=>{
                sessionStorage.setItem("config", JSON.stringify(data));
            });
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
                    Please Login.
                </div>
            );
        }
    }
}
