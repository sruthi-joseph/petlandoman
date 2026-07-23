import {defineCliConfig} from 'sanity/cli'

export default defineCliConfig({
  api: {
    projectId: '1dvvzwi3',
    dataset: 'production'
  },
  deployment: {
    autoUpdates: true,
  },
  vite: (config) => {
    return {
      ...config,
      base: '/studio/',
    }
  }
})
