
// ui_trial2.h : main header file for the PROJECT_NAME application
//

#pragma once

#ifndef __AFXWIN_H__
	#error "include 'pch.h' before including this file for PCH"
#endif

#include "resource.h"		// main symbols


// Cuitrial2App:
// See ui_trial2.cpp for the implementation of this class
//

class Cuitrial2App : public CWinApp
{
public:
	Cuitrial2App();

// Overrides
public:
	virtual BOOL InitInstance();

// Implementation

	DECLARE_MESSAGE_MAP()
};

extern Cuitrial2App theApp;
