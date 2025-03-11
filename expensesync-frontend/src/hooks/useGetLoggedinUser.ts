import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";

const useGetLoggedinUser = () => {
    const {data} = useGetUserQuery();
    if(data){
        return data
    }
    return null;
};
export default useGetLoggedinUser;
