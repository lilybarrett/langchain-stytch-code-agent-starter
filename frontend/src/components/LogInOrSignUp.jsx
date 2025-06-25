// import { StytchB2B } from "@stytch/react/b2b";
// import { discoveryConfig, discoveryStyles } from '../utils/stytchConfig';
import { StytchEventType } from '@stytch/vanilla-js';
import { useNavigate } from 'react-router-dom';

import { StytchB2B } from '@stytch/react/b2b';
import { AuthFlowType, B2BProducts } from '@stytch/vanilla-js/b2b';

export const LogInOrSignUp = () => {
  const navigate = useNavigate();
   const config = {
      products: [B2BProducts.emailMagicLinks],
      sessionOptions: { sessionDurationMinutes: 60 },
      authFlowType: AuthFlowType.Discovery,
    };

   return <StytchB2B
      config={config}
      callbacks={{
        onEvent: (event) => {
          if (event.type === StytchEventType.AuthenticateFlowComplete) {
            navigate('/dashboard', { replace: true });
          }
        },
      }}
    />;
};

// export const LoginOrSignup = () => {
//   const navigate = useNavigate();

//   return (
//     <div className="centered-login">
//       <StytchB2B
//     //   config={discoveryConfig}
//     //   styles={discoveryStyles}
    //   callbacks={{
    //     onEvent: (event) => {
    //       if (event.type === StytchEventType.AuthenticateFlowComplete) {
    //         navigate('/dashboard', { replace: true });
    //       }
    //     },
    //   }}
//       />
//     </div>
//   );
// };