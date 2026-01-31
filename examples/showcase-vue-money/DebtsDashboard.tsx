import React from 'react';

/**
 * 🛡️ Vue Money - Safe Feature Addition Example
 * Requirement: Add a new "Credit Cards" section without breaking the existing app.
 */

// 1. Define your Feature Flag Logic (Mock or Real SDK)
const FeatureFlags = {
    isEnabled: (flagName: string) => {
        // In production, this would call LaunchDarkly or a custom backend
        const config = {
            'enable-credit-cards': false, // Still in dev!
        };
        return config[flagName] || false;
    }
};

// 2. The Legacy Component (Untouched)
const LegacyLoanList = () => (
    <div className="p-4 border border-blue-200 bg-blue-50 rounded-xl">
        <h2 className="text-blue-800 font-bold">🏦 Active Auto Loans</h2>
        <p className="text-blue-600">No active loans found.</p>
    </div>
);

// 3. The New Component (Independent)
const CreditCardSection = () => (
    <div className="p-4 mt-4 border border-purple-200 bg-purple-50 rounded-xl animate-pulse">
        <h2 className="text-purple-800 font-bold">💳 New: Credit Cards (Beta)</h2>
        <p className="text-purple-600 italic">This section is only visible to testers.</p>
    </div>
);

// 4. The "Safety Wrapper" Deployment
export const DebtsDashboard = () => {
    const showCreditCards = FeatureFlags.isEnabled('enable-credit-cards');

    return (
        <div className="space-y-4">
            <h1 className="text-2xl font-bold">My Debts</h1>

            {/* 🚀 ELITE PATTERN: Keep legacy code running as the primary path */}
            <LegacyLoanList />

            {/* 🛡️ Guarded additions */}
            {showCreditCards && <CreditCardSection />}

            {!showCreditCards && (
                <p className="text-xs text-gray-400">
                    Check back soon for Credit Card support.
                </p>
            )}
        </div>
    );
};

export default DebtsDashboard;
