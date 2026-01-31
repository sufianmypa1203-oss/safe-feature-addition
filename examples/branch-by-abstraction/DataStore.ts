// examples/branch-by-abstraction/DataStore.ts

/**
 * The Abstraction Layer
 */
interface IDataStore {
    getUser(id: string): Promise<any>;
}

/**
 * Old Implementation (Legacy API)
 */
class LegacyApiStore implements IDataStore {
    async getUser(id: string) {
        console.log('[Legacy] Fetching from REST API...');
        return { id, source: 'rest' };
    }
}

/**
 * New Implementation (GraphQL)
 */
class NewGraphQLStore implements IDataStore {
    async getUser(id: string) {
        console.log('[New] Fetching from GraphQL...');
        return { id, source: 'graphql' };
    }
}

/**
 * The Router
 */
export class DataStoreFactory {
    static getStore(useNew: boolean): IDataStore {
        return useNew ? new NewGraphQLStore() : new LegacyApiStore();
    }
}

// Usage in application code
const store = DataStoreFactory.getStore(process.env.USE_NEW_STORE === 'true');
store.getUser('123');
