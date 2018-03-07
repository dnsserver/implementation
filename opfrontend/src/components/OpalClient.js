import React, {Component} from 'react';

import { OpalAPI } from '../utils/opal-api';

export default class OpalClient extends Component {
    constructor(props){
        super(props);
        const sess = JSON.parse(sessionStorage.getItem('session'));
        const cfg = JSON.parse(sessionStorage.getItem('config'));
        this.state = {
            config: cfg,
            session: sess,
            name: null,
            description: null,
            oidc_request: null,
            oidc_response: null
        };

    }

    // doLogin(config, ){
    //     const config = this.state.config;
    //     const opalAPI = new OpalAPI();
    //     const id = 'name';
    //     if(config && config.auth_uri){
    //         opalAPI.redirectForLogin(config, '/opal_oidc/'+id);
    //     }else{
    //         NotificationManager.error("Please provide a configuration first.", '', 3000);
    //     }
    //
    // }

    componentDidMount() {
        const config = this.state.config;
        const session = this.state.session;
        if(this.props.match.params.id){

            const id = this.props.match.params.id;
            const opalAPI = new OpalAPI();

            const params = new URLSearchParams(this.props.location.search);
            const code = params.get('code');
            if(code){
                opalAPI.getAccessToken(config, code).then((data)=>{
                    console.log(data);
                });
            }else{
                opalAPI.getClient(config.opal_data_provider, session.access_token, id).then((data)=>{
                    const name = data["name"];
                    const desc = data["description"];
                    const oidc_request = JSON.parse(data["oidc_request"]);
                    const oidc_response= JSON.parse(data["oidc_response"]);
                    this.setState({
                        name: name,
                        description: desc,
                        oidc_request: oidc_request,
                        oidc_response: oidc_response
                    });

                    const client_cfg = {
                        "auth_uri":config.auth_uri,
                        "client_id":oidc_response["client_id"],
                        "scopes":oidc_response["scope"]
                    }
                    opalAPI.redirectForLogin(client_cfg, oidc_response["redirect_uris"][0]);
                });
            }
        }
    }

    render(){
        return (
            <div>
                <p>OPAL Client</p>
                <div className="row">
                    <div className="col-sm-12">
                        <h5 className="mb-1">{this.state.name}</h5>
                        <small className="text-muted">{this.state.description}</small>
                    </div>
                    <div className="col-sm-12">
                        <pre>
                            {JSON.stringify(this.state.oidc_request, null, "  ")}
                        </pre>
                    </div>
                    <div className="col-sm-12">
                        <pre>
                            {JSON.stringify(this.state.oidc_response, null, "  ")}
                        </pre>
                    </div>
                </div>
            </div>);
    }
}
