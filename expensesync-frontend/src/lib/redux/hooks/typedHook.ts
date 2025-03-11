import type { AppDispatch, AppStore, RootState } from "../store";
// import type {TypedUseSelectorHook} from "react-redux"
import { useDispatch, useSelector, useStore } from "react-redux";

// export const useAppDispatch: () => AppDispatch = useDispatch
// export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
// export const useAppStore: () => AppStore = useStore

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = useDispatch.withTypes<AppDispatch>()
export const useAppSelector = useSelector.withTypes<RootState>()
export const useAppStore = useStore.withTypes<AppStore>()