"use client"
import { AppStore, makeStore } from "./store"
import React, { useRef } from "react"
import { Provider } from "react-redux"

interface ProviderProps {
    children: React.ReactNode
}

export default function ReduxProvider({children}: ProviderProps) {
    const storeRef = useRef<AppStore>(undefined)
    if (!storeRef.current){
        // Create the store instance the first time this renders
        storeRef.current = makeStore()
    }
    return(
        <Provider store={storeRef.current}>{children}</Provider>
    )
}