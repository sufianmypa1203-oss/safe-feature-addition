// examples/strangler-fig/gateway.js
const express = require('express');
const app = express();

const LEGACY_URL = 'http://legacy-monolith:8080';
const NEW_SERVICE_URL = 'http://new-payment-service:3000';

/**
 * Strangler Fig Gateway
 * Gradually routes traffic from the old monolith to the new microservice.
 */

app.use('/api/payments', (req, res, next) => {
    // Phase 1: Use a feature flag or a percentage trial
    const useNewService = Math.random() < 0.25; // 25% traffic

    if (useNewService) {
        console.log('[Gateway] Routing to NEW payment service');
        // Proxy logic here (e.g., using http-proxy-middleware)
        res.redirect(307, `${NEW_SERVICE_URL}${req.url}`);
    } else {
        console.log('[Gateway] Routing to LEGACY monolith');
        res.redirect(307, `${LEGACY_URL}${req.url}`);
    }
});

app.listen(80, () => console.log('Strangler Fig Gateway running on port 80'));
