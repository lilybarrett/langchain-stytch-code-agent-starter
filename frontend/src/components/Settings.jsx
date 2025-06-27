import { AdminPortalOrgSettings } from '@stytch/react/b2b/adminPortal';
import { adminPortalConfig, adminPortalStyles } from '../utils/stytchConfig';

export const Settings = () => {
  return <AdminPortalOrgSettings styles={adminPortalStyles} config={adminPortalConfig} />;
};
