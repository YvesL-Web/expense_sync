import React, { useEffect, useState } from 'react';
import { usePlaidLink } from 'react-plaid-link';

const PlaidLinkButton = () => {
    const [linkToken, setLinkToken] = useState(null);

    // Récupérer le link_token depuis l'API Django
    useEffect(() => {
        const fetchLinkToken = async () => {
            const response = await fetch('http://localhost:8000/create_link_token/');
            const data = await response.json();
            setLinkToken(data.link_token);
        };
        fetchLinkToken();
    }, []);

    const onSuccess = async (publicToken) => {
        // Échanger le public_token contre un access_token
        const response = await fetch('http://localhost:8000/get_access_token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ public_token: publicToken }),
        });
        const data = await response.json();
        console.log('Access Token:', data.access_token);
    };

    const config = {
        token: linkToken,
        onSuccess,
    };

    const { open, ready } = usePlaidLink(config);

    return (
        <button onClick={() => open()} disabled={!ready}>
            Connecter un compte bancaire
        </button>
    );
};

export default PlaidLinkButton;