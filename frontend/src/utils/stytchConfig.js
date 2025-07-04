import { AdminPortalB2BProducts } from '@stytch/react/b2b/adminPortal';
import { AuthFlowType, B2BProducts, B2BOAuthProviders } from '@stytch/vanilla-js';

export const adminPortalConfig = {
  allowedAuthMethods: [
    AdminPortalB2BProducts.emailMagicLinks,
    AdminPortalB2BProducts.sso,
    AdminPortalB2BProducts.oauthGoogle,
  ],
};

export const discoveryConfig = {
  products: [B2BProducts.sso, B2BProducts.oauth, B2BProducts.emailMagicLinks],
  sessionOptions: { sessionDurationMinutes: 60 },
  oauthOptions: {
    providers: [{ type: B2BOAuthProviders.Google }],
  },
  authFlowType: AuthFlowType.Discovery,
};

export const adminPortalStyles = {
  fontFamily: 'IBM Plex Sans',
};

export const discoveryStyles = {
  fontFamily: 'IBM Plex Sans',
  container: {
    width: '500px',
  },
};
