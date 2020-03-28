///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Apr 24 2017)
// http://www.wxformbuilder.org/
//
// PLEASE DO "NOT" EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "noname.h"

///////////////////////////////////////////////////////////////////////////

MyFrame1::MyFrame1( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );
	
	wxGridBagSizer* gbSizer1;
	gbSizer1 = new wxGridBagSizer( 0, 0 );
	gbSizer1->SetFlexibleDirection( wxBOTH );
	gbSizer1->SetNonFlexibleGrowMode( wxFLEX_GROWMODE_SPECIFIED );
	
	m_button1 = new wxButton( this, wxID_ANY, wxT("MyButton"), wxDefaultPosition, wxDefaultSize, 0 );
	gbSizer1->Add( m_button1, wxGBPosition( 0, 0 ), wxGBSpan( 1, 1 ), wxALL, 5 );
	
	m_staticText1 = new wxStaticText( this, wxID_ANY, wxT("MyLabel"), wxDefaultPosition, wxDefaultSize, 0 );
	m_staticText1->Wrap( -1 );
	gbSizer1->Add( m_staticText1, wxGBPosition( 0, 1 ), wxGBSpan( 1, 1 ), wxALL, 5 );
	
	m_textCtrl1 = new wxTextCtrl( this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0 );
	gbSizer1->Add( m_textCtrl1, wxGBPosition( 0, 2 ), wxGBSpan( 1, 1 ), wxALL, 5 );
	
	
	this->SetSizer( gbSizer1 );
	this->Layout();
	
	this->Centre( wxBOTH );
}

MyFrame1::~MyFrame1()
{
}
