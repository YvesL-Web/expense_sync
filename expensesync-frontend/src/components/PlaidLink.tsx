import React, { useCallback, useEffect, useState } from 'react'
import { Button } from './ui/button'
import { PlaidLinkOnSuccess, PlaidLinkOptions, usePlaidLink } from 'react-plaid-link'
import { useRouter } from 'next/navigation';

// import { exchangePublicToken } from '@/lib/actions/user.actions';
import Image from 'next/image';
import { PlaidLinkProps } from '@/types';
import { useCreatePlaidLinkTokenMutation, useExchangePublicTokenMutation } from '@/lib/redux/features/account/bankAccountApiSlice';

const PlaidLink = ({variant}: PlaidLinkProps) => {
  const router = useRouter();
  const [createPlaidLinkToken] = useCreatePlaidLinkTokenMutation()
  const [exchangePublicToken] = useExchangePublicTokenMutation()
  const [token, setToken] = useState('');

  useEffect(() => {
    const getLinkToken = async () => {
      const data = await createPlaidLinkToken().unwrap();
      setToken(data?.link_token);
    }
    getLinkToken();
  }, [createPlaidLinkToken]);


  const onSuccess = useCallback<PlaidLinkOnSuccess>(async (public_token: string) => {
    // send public_token to server
    await exchangePublicToken({
      public_token: public_token,
    }).unwrap()
    router.push('/');
  }, [])
  
  const config: PlaidLinkOptions = {
    token,
    onSuccess
  }

  const { open, ready } = usePlaidLink(config);
  
  return (
    <>
      {variant === 'primary' ? (
        <Button
          onClick={() => open()}
          disabled={!ready}
          className="plaidlink-primary"
        >
          Connect bank
        </Button>
      ): variant === 'ghost' ? (
        <Button onClick={() => open()} variant="ghost" className="plaidlink-ghost">
          <Image 
            src="/icons/connect-bank.svg"
            alt="connect bank"
            width={24}
            height={24}
          />
          <p className='hiddenl text-[16px] font-semibold text-black-2 xl:block'>Connect bank</p>
        </Button>
      ): (
        <Button onClick={() => open()} className="plaidlink-default">
          <Image 
            src="/icons/connect-bank.svg"
            alt="connect bank"
            width={24}
            height={24}
          />
          <p className='text-[16px] font-semibold text-black-2'>Connect bank</p>
        </Button>
      )}
    </>
  )
}

export default PlaidLink