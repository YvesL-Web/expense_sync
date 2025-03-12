import React, { useCallback, useEffect, useState } from 'react'
import { Button } from './ui/button'
import { PlaidLinkOnSuccess, PlaidLinkOnSuccessMetadata, PlaidLinkOptions, usePlaidLink } from 'react-plaid-link'
import { useRouter } from 'next/navigation';

// import { exchangePublicToken } from '@/lib/actions/user.actions';
import Image from 'next/image';
import { PlaidLinkProps } from '@/types';
import { useCreatePlaidLinkTokenMutation, useExchangePublicTokenMutation } from '@/lib/redux/features/account/bankAccountApiSlice';
import { toast } from 'sonner';
import extractErrorMessage from '@/utils/extractErrorMessage';

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
  }, []);


  const onSuccess = useCallback<PlaidLinkOnSuccess>(async (public_token: string, metadata: PlaidLinkOnSuccessMetadata) => {
    // send public_token to server
    try {
      await exchangePublicToken({
        public_token: public_token,
        metadata: {
          institution: {
            name: metadata.institution?.name || '',
            institution_id: metadata.institution?.institution_id || ''
          }
        }
      }).unwrap()
      toast.success("Account successfully linked.")
      router.push('/');
    } catch (error) {
      const errorMessage=extractErrorMessage(error) 
      toast.error(errorMessage)
    }
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