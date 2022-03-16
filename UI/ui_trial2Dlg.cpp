// ui_trial2Dlg.cpp : implementation file
//

#include "pch.h"
#include "framework.h"
#include "ui_trial2.h"
#include "ui_trial2Dlg.h"
#include "afxdialogex.h"
#include "opencv2/opencv.hpp"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif
#define TID_ONLY_ONCE WM_USER + 202

// Cuitrial2Dlg dialog


Cuitrial2Dlg::Cuitrial2Dlg(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_UI_TRIAL2_DIALOG, pParent)
	, m_path(_T(""))
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void Cuitrial2Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_PICTURE, m_picture);
	DDX_Text(pDX, IDC_EDIT1, m_path);
	DDX_Control(pDX, IDC_PLOT, m_plot);
}

BEGIN_MESSAGE_MAP(Cuitrial2Dlg, CDialogEx)
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_WM_DESTROY()
	ON_WM_TIMER()
	
	ON_BN_CLICKED(IDC_OPEN, &Cuitrial2Dlg::OnBnClickedOpen)
	ON_BN_CLICKED(IDC_SEARCH, &Cuitrial2Dlg::OnBnClickedSearch)
END_MESSAGE_MAP()


// Cuitrial2Dlg message handlers

BOOL Cuitrial2Dlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	// TODO: Add extra initialization here
	

	return TRUE;  // return TRUE  unless you set the focus to a control
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void Cuitrial2Dlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rect1angle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect1;
		GetClientRect(&rect1);
		int x = (rect1.Width() - cxIcon + 1) / 2;
		int y = (rect1.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR Cuitrial2Dlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void Cuitrial2Dlg::OnDestroy()
{
	CDialogEx::OnDestroy();

	// TODO: Add your message handler code here
}


void Cuitrial2Dlg::OnTimer(UINT_PTR nIDEvent)
{
	// TODO: Add your message handler code here and/or call default
	
	if (nIDEvent == TID_ONLY_ONCE)
	{
		KillTimer(TID_ONLY_ONCE);
		//system("pause");
		Invalidate();
		
		//SomethingLongProcess(pSomeData);
	}
	
	Mat pframe,pout;
	if (frame_count > (nframes - 1))
		cap.set(CAP_PROP_POS_FRAMES,nframes-2);

	cap >> pframe;
	//separate colors && picks up blueish colored area
	vector<Mat> bgr_planes;
	split(pframe, bgr_planes);
	tm1 = (bgr_planes[0] < 200);
	tm2 = (bgr_planes[0] > 49);
	bitwise_and(tm1, tm2, tmp_1);
	tm3 = (bgr_planes[2] < 90);
	bitwise_and(tmp_1, tm3,pout);
	if (frame_count == 0)
	{
		pout.copyTo(scoreout);
		imwrite("./org.png", scoreout);
	}
	else if(frame_count<nframes-10)
	{
		bitwise_and(pout, scoreout, scoreout);
	}
	else if (frame_count == nframes - 5)
	{
		
		imwrite("./out.png", scoreout);
		remained = int(sum(scoreout)[0]);
		score = round(100 * remained / tot_lane);
		printf("%d", score);
		
		//putText(p0, "", Point(50, 50), FONT_HERSHEY_SIMPLEX, Scalar(255, 0,0));
		
	}
	//count the filtered area and save data
	double result_lane = (int)sum(pout)[0];
	if (frame_count == 0)
		tot_lane = result_lane;
	double result_steppedOn = tot_lane - result_lane;
	bad_score.resize(size_t(frame_count + 1));
	accumulated.resize(size_t(frame_count + 1));
	bad_score.at(frame_count) = result_steppedOn;
	tot += result_steppedOn;
	accumulated.at(frame_count)= tot;
	//int y = round(100000 * result_steppedOn / (tot_lane*0.5));
	//int y = round( tot/(tot_lane*100.0));
	double y = round(800*result_steppedOn/tot_lane );
	if (y >= 1000)y = 800;
	circle(p0, Point(frame_count,800-10*y), 3, Scalar(0, 0, 255), -1, LINE_AA);
	
	
	//create rgb color Mat form of the filtered area result
	bgr_planes.clear();
	vector<Mat> tempback;
	tempback = {pout,pout,pout };
	merge(tempback, out);

	//horizontal merge with original frame and the processed one
	hconcat(pframe, out, frame);

	//from Mat to bitmap image for PICUTRE CONTROL panels
	int bpp = 8 * frame.elemSize();
	assert((bpp == 8 || bpp == 24 || bpp == 32));
	int padding = 0;
	//32 bit image is always DWORD aligned because each pixel requires 4 bytes
	if (bpp < 32)
		padding = 4 - (frame.cols % 4);
	if (padding == 4)
		padding = 0;
	int border = 0;
	//32 bit image is always DWORD aligned because each pixel requires 4 bytes
	if (bpp < 32)
	{
		border = 4 - (frame.cols % 4);
	}
	Mat mat_temp;
	if (border > 0 || frame.isContinuous() == false)
	{
		// Adding needed columns on the right (max 3 px)
		cv::copyMakeBorder(frame, mat_temp, 0, 0, 0, border, cv::BORDER_CONSTANT, 0);
	}
	else
	{
		mat_temp = frame;
	}

	RECT rect;
	m_picture.GetClientRect(&rect);
	cv::Size winSize(rect.right, rect.bottom);
	img_frame.Create(winSize.width, winSize.height, 24);



	
	//**********************************************************************************************************
	//                      FRAME
	//**********************************************************************************************************

	BITMAPINFO* bitInfo = (BITMAPINFO*)malloc(sizeof(BITMAPINFO) + 256 * sizeof(RGBQUAD));

	bitInfo->bmiHeader.biBitCount = bpp;
	bitInfo->bmiHeader.biWidth = mat_temp.cols;
	bitInfo->bmiHeader.biHeight = -mat_temp.rows;
	bitInfo->bmiHeader.biPlanes = 1;
	bitInfo->bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	bitInfo->bmiHeader.biCompression = BI_RGB;
	bitInfo->bmiHeader.biClrImportant = 0;
	bitInfo->bmiHeader.biClrUsed = 0;
	bitInfo->bmiHeader.biSizeImage = 0;
	bitInfo->bmiHeader.biXPelsPerMeter = 0;
	bitInfo->bmiHeader.biYPelsPerMeter = 0;


	if (mat_temp.cols == winSize.width && mat_temp.rows == winSize.height)
	{
		// source and destination have same size
		// transfer memory block
		// NOTE: the padding border will be shown here. Anyway it will be max 3px width

		SetDIBitsToDevice(img_frame.GetDC(),
			//destination rect1angle
			0, 0, winSize.width, winSize.height,
			0, 0, 0, mat_temp.rows,
			mat_temp.data, bitInfo, DIB_RGB_COLORS);
	}
	else
	{
		// destination rect1angle
		int destx = 0, desty = 0;
		int destw = winSize.width;
		int desth = winSize.height;

		// rect1angle defined on source bitmap
		// using imgWidth instead of mat_temp.cols will ignore the padding border
		int imgx = 0, imgy = 0;
		int imgWidth = mat_temp.cols - border;
		int imgHeight = mat_temp.rows;

		StretchDIBits(img_frame.GetDC(),
			destx, desty, destw, desth,
			imgx, imgy, imgWidth, imgHeight,
			mat_temp.data, bitInfo, DIB_RGB_COLORS, SRCCOPY);
	}





	//********************************************
	//from Mat to bitmap image for PICUTRE CONTROL panels
	int bpp1 = 8 * p0.elemSize();
	assert((bpp1 == 8 || bpp1 == 24 || bpp1 == 32));
	int padding1 = 0;
	//32 bit image is always DWORD aligned because each pixel requires 4 bytes
	if (bpp1 < 32)
		padding1 = 4 - (p0.cols % 4);
	if (padding1 == 4)
		padding1 = 0;
	int border1 = 0;
	//32 bit image is always DWORD aligned because each pixel requires 4 bytes
	if (bpp1 < 32)
	{
		border1 = 4 - (p0.cols % 4);
	}
	Mat mat_temp1;
	if (border1 > 0 || p0.isContinuous() == false)
	{
		// Adding needed columns on the right (max 3 px)
		cv::copyMakeBorder(p0, mat_temp1, 0, 0, 0, border1, cv::BORDER_CONSTANT, 0);
	}
	else
	{
		mat_temp1 = p0;
	}

	RECT rect1;
	m_plot.GetClientRect(&rect1);
	cv::Size winSize1(rect1.right, rect1.bottom);
	img_p0.Create(winSize1.width, winSize1.height, 24);

	//**********************************************************************************************************
	//                      PLOT
	//**********************************************************************************************************

	BITMAPINFO* bitinfo1 = (BITMAPINFO*)malloc(sizeof(BITMAPINFO) + 256 * sizeof(RGBQUAD));

	bitinfo1->bmiHeader.biBitCount = bpp1;
	bitinfo1->bmiHeader.biWidth = mat_temp1.cols;
	bitinfo1->bmiHeader.biHeight = -mat_temp1.rows;
	bitinfo1->bmiHeader.biPlanes = 1;
	bitinfo1->bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	bitinfo1->bmiHeader.biCompression = BI_RGB;
	bitinfo1->bmiHeader.biClrImportant = 0;
	bitinfo1->bmiHeader.biClrUsed = 0;
	bitinfo1->bmiHeader.biSizeImage = 0;
	bitinfo1->bmiHeader.biXPelsPerMeter = 0;
	bitinfo1->bmiHeader.biYPelsPerMeter = 0;


	if (mat_temp1.cols == winSize1.width && mat_temp1.rows == winSize1.height)
	{
		// source and destination have same size
		// transfer memory block
		// NOTE: the padding border will be shown here. Anyway it will be max 3px width

		SetDIBitsToDevice(img_p0.GetDC(),
			//destination rect1angle
			0, 0, winSize1.width, winSize1.height,
			0, 0, 0, mat_temp1.rows,
			mat_temp1.data, bitinfo1, DIB_RGB_COLORS);
	}
	else
	{
		// destination rect1angle
		int destx1 = 0, desty1 = 0;
		int destw1 = winSize1.width;
		int desth1 = winSize1.height;

		// rect1angle defined on source bitmap
		// using imgWidth1 instead of mat_temp1.cols will ignore the padding border
		int imgx1 = 0, imgy1 = 0;
		int imgWidth1 = mat_temp1.cols - border;
		int imgHeight1 = mat_temp1.rows;

		StretchDIBits(img_p0.GetDC(),
			destx1, desty1, destw1, desth1,
			imgx1, imgy1, imgWidth1, imgHeight1,
			mat_temp1.data, bitinfo1, DIB_RGB_COLORS, SRCCOPY);
	}



	//**********************************************************************************************************




	HDC dc = ::GetDC(m_picture.m_hWnd);
	img_frame.BitBlt(dc, 0, 0);
	::ReleaseDC(m_picture.m_hWnd, dc);
	img_frame.ReleaseDC();
	img_frame.Destroy();



	HDC dc1 = ::GetDC(m_plot.m_hWnd);
	img_p0.BitBlt(dc1, 0, 0);
	::ReleaseDC(m_plot.m_hWnd, dc1);
	img_p0.ReleaseDC();
	img_p0.Destroy();




	frame_count++;
	if (frame_count == nframes)
	{
		frame_count = 0;
		nIDEvent = TID_ONLY_ONCE;
		MessageBox(_T("The Score is ..."));		
		KillTimer(0);
	}

	CDialogEx::OnTimer(nIDEvent);

}





void Cuitrial2Dlg::OnBnClickedOpen()
{
	// TODO: Add your control notification handler code here
	CT2CA pszString(m_path);
	std::string strPath(pszString);
	cap.open(strPath);
	if (!cap.isOpened()) {
		MessageBox(_T("Video is Not available!"));
		cerr << "[ERROR]" << endl;
	}
	
	//nframes = cap.get(CAP_PROP_FRAME_COUNT);
	if (m_path.Find('3')) nframes = 482;
	else if (m_path.Find('1')) nframes = 545;
	Mat pp0(1000, nframes, CV_8UC3);
	pp0.copyTo(p0);
	p0.setTo(Scalar(255,255,255));
	//pp0.copyTo(p1);
	//pp0.copyTo(p2);
	//pp0.copyTo(p3);
	pp0.copyTo(pfinal);

	tot = 0;
	bad_score.clear();
	accumulated.clear();
	frame_count = 0;
	SetTimer(0, 10, NULL);// every10ms
}


void Cuitrial2Dlg::OnBnClickedSearch()
{
	// TODO: Add your control notification handler code here

	CString str = _T("All files(*.*)|*.*|"); 
	CFileDialog dlg(TRUE, _T("*.avi"), NULL, OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT, str, this);
	if (dlg.DoModal() == IDOK)
	{
		m_path = dlg.GetPathName();

		SetDlgItemText(IDC_EDIT1,m_path);
	}

}
