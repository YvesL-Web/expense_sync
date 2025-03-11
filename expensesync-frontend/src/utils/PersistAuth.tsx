"use client";

import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { getCookie } from "cookies-next";
import { setAuth, setLogout } from "@/lib/redux/features/auth/authSlice";

const PersistAuth = () => {
	const dispatch = useDispatch();

	useEffect(() => {
		const isLoggedIn = getCookie("logged_in") === "true";
		if (isLoggedIn) {
			dispatch(setAuth());
		} else {
			dispatch(setLogout());
		}
	}, [dispatch]);

	return null;
};
export default PersistAuth;
