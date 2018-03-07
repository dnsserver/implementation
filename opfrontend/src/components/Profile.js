import React, {Component} from 'react';

import { OpalAPI } from '../utils/opal-api';

export default class Profile extends Component {
    constructor(props){
        super(props);
        const sess = JSON.parse(sessionStorage.getItem('session'));
        const cfg = JSON.parse(sessionStorage.getItem('config'));
        this.state = {
            config: cfg,
            session: sess,
            profile: {}
        };
    }

    componentDidMount() {
        let opalAPI = new OpalAPI();
        opalAPI.getUserInfo(this.state.config.userinfo_uri, this.state.session.access_token).then((data)=>{
            this.setState({
                profile: data
            });
        });
    }

    render(){
        return (
            <div>
            <pre>
                {JSON.stringify(this.state.profile)}
            </pre>
            </div>);
    }
}
