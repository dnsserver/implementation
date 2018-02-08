import React, { Component } from 'react';
import {NotificationManager} from 'react-notifications';

import { OpalAPI } from '../utils/opal-api';

export default class OIDC extends Component {
    constructor(props){
        super(props);
        let cfg = sessionStorage.getItem('config');
        if(!cfg){
            cfg = `{
    "base_url":"http://localhost:3000",
    "redirect_uri":"/oidc_callback",
    "scopes": "openid profile",
    "client_id": "",
    "client_secret": "",
    "auth_uri":"http://localhost:8085/openid-connect-server-webapp/authorize",
    "token_uri":"http://localhost:8085/openid-connect-server-webapp/token",
    "userinfo_uri":"http://localhost:8085/openid-connect-server-webapp/userinfo",
    "issuer":"http://localhost:8085/openid-connect-server-webapp/",
    "token_introspection_uri":"http://localhost:8085/openid-connect-server-webapp/introspect",
    "registration_uri":"http://localhost:8085/openid-connect-server-webapp/register"
}`;
        }
        this.state = {
            config: cfg
        };
        this.handleConfigSubmit = this.handleConfigSubmit.bind(this);
        this.handleConfigChange = this.handleConfigChange.bind(this);
        this.redirectForLogin = this.redirectForLogin.bind(this);

        const cObj = JSON.parse(cfg);
        if(props.location.pathname === cObj.redirect_uri){
            const params = new URLSearchParams(props.location.search);
            const code = params.get('code');
            if(code){
                let opalAPI = new OpalAPI();
                opalAPI.getAccessToken(cObj, code).then((data)=>{
                    console.log(data);
                })
            }
        }
    }

    handleConfigChange(e){
        this.setState({config: e.target.value});
    }

    handleConfigSubmit(e){
        e.preventDefault();
        if(this.props.onSaveConfiguration){
            this.props.onSaveConfiguration(this.state.config);
        }
        NotificationManager.info("Configuration saved.", '', 3000);
    }

    redirectForLogin(){
        const config = JSON.parse(this.state.config);
        console.log(config);
        if(config && config.auth_uri){
            var q = new URLSearchParams();
            q.set('client_id', config.client_id);
            q.set('redirect_uri', config.base_url+'/oidc_callback');
            q.set('scope', config.scopes);
            q.set('response_type','code');
            q.set('openid.realm', config.base_url+'/oidc_callback');

            window.location = config.auth_uri +"?"+ q.toString();
        }else{
            NotificationManager.error("Please provide a configuration first.", '', 3000);
        }

    }

    render(){
        return (<div>
            <div>
                Configuration for OIDC in json format.
            </div>
            <br/>
            <form onSubmit={this.handleConfigSubmit}>
                <div className="form-group">
                    <label htmlFor="config">Configuration</label>
                    <textarea className="form-control" id="config"
                        value={this.state.config}
                        onChange={this.handleConfigChange}/>
                </div>
                <button type="submit" className="btn btn-default">Save</button>
            </form>
            <button type="button" className="btn btn-default" onClick={this.redirectForLogin}>Login</button>
            </div>);
    }
}
