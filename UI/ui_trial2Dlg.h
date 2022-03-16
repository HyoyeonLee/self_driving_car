
// ui_trial2Dlg.h : header file
//

#pragma once

#include "opencv2/opencv.hpp"
#include<opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include<opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
using namespace cv;
using namespace std;
// Cuitrial2Dlg dialog
class Cuitrial2Dlg : public CDialogEx
{
// Construction
public:
	Cuitrial2Dlg(CWnd* pParent = nullptr);	// standard constructor

// Dialog Data
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_UI_TRIAL2_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CStatic m_picture;
	afx_msg void OnDestroy();
	afx_msg void OnTimer(UINT_PTR nIDEvent);
	
	//*******************************************add
	VideoCapture cap;
	Mat frame, src, out, tm1, tm2, tm3, tmp_1,scoreout;
	CImage img_frame, img_out,img_p0,img_out1;
	int nframes,frame_count;
	vector<double> bad_score;
	vector<double> accumulated;
	double tot;
	double tot_lane;
	Mat p0, p1, p2, p3,pfinal;
	double remained;
	int score;

	afx_msg void OnBnClickedFileopen();
	afx_msg void OnBnClickedOpen();
	afx_msg void OnBnClickedSearch();
	CString m_path;
	CStatic m_plot;
};
