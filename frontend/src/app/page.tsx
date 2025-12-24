"use client";

import React from 'react';
import NerveCenterLayout from '../components/layouts/nerve-center';

export default function Home() {
  return (
    <NerveCenterLayout>
        {/* Children can be used for secondary overlays or specific route content */}
        <div className="hidden">Living Dashboard Initialized</div>
    </NerveCenterLayout>
  );
}