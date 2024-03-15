//******************************************************************************
//* Copyright (c) 2017 Ford Motor Company. All Rights Reserved.
//******************************************************************************
package com.ford.wings.outbound;

import java.math.BigInteger;
import java.util.Date;
import java.util.List;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;

import com.ford.wings.inbound.WingsBaseAuditTO;
import com.ford.wings.inbound.admin.PaginationTO;
import com.ford.wings.inbound.admin.StatusTO;
import com.ford.wings.inbound.inbound.PartsXWarehouseTO;

/**
 * @author mtorre94
 * Initial version generated by codequick
 *
 */
/**
 * @author Souza, Emerson
 *
 */
public class DenialTO extends WingsBaseAuditTO {

	// Properties
	private java.math.BigInteger denialUidK;

	@NotNull
	private java.math.BigInteger partWhUidD;

	@NotNull
	private java.math.BigInteger statusUidD;

	@NotNull @Pattern(regexp="^(?!\\s*$).+")
	private String openC;

	@NotNull
	private java.util.Date openS;

	private String printedC;

	private java.util.Date printedS;

	private String closeC;

	private java.util.Date closeS;

	private java.math.BigInteger denialQ;

	private java.math.BigInteger countedQ;

	private java.math.BigInteger currentQ;

	private java.math.BigInteger allocatedQ;

	private java.math.BigInteger otherQ;

	private String locationC;

	private String stockTypeN;

	private java.util.Date startS;

	private java.util.Date endS;

	private BigInteger bkSubDivisionUidD;

    private String denialLabel;

    private BigInteger locationQuantity;

	private PartsXWarehouseTO partsXWarehouse;

	private StatusTO statusTO;
		
	private PaginationTO pagination = new PaginationTO();

	private List<java.math.BigInteger> denialSearch;
	
	private String countryTimeZoneC;
	
	// Getters and Setters
	public java.math.BigInteger getDenialUidK() {
		return denialUidK;
	}

	public void setDenialUidK(java.math.BigInteger denialUidK) {
		this.denialUidK = denialUidK;
	}
    
	public List<java.math.BigInteger> getDenialSearch() {
		return denialSearch;
	}

	public void setDenialSearch(List<java.math.BigInteger> denialSearch) {
		this.denialSearch = denialSearch;
	}

	public java.math.BigInteger getPartWhUidD() {
		return partWhUidD;
	}

	public void setPartWhUidD(java.math.BigInteger partWhUidD) {
		this.partWhUidD = partWhUidD;
	}
    
	public java.math.BigInteger getStatusUidD() {
		return statusUidD;
	}

	public void setStatusUidD(java.math.BigInteger statusUidD) {
		this.statusUidD = statusUidD;
	}
    
	public String getOpenC() {
		return openC;
	}

	public void setOpenC(String openC) {
		this.openC = openC;
	}
    
	public java.util.Date getOpenS() {
		return openS;
	}

	public void setOpenS(java.util.Date openS) {
		this.openS = openS;
	}
    
	public String getPrintedC() {
		return printedC;
	}

	public void setPrintedC(String printedC) {
		this.printedC = printedC;
	}
    
	public java.util.Date getPrintedS() {
		return printedS;
	}

	public void setPrintedS(java.util.Date printedS) {
		this.printedS = printedS;
	}
    
	public String getCloseC() {
		return closeC;
	}

	public void setCloseC(String closeC) {
		this.closeC = closeC;
	}
    
	public java.util.Date getCloseS() {
		return closeS;
	}

	public void setCloseS(java.util.Date closeS) {
		this.closeS = closeS;
	}
    
	public java.math.BigInteger getDenialQ() {
		return denialQ;
	}

	public void setDenialQ(java.math.BigInteger denialQ) {
		this.denialQ = denialQ;
	}
    
	public java.math.BigInteger getCountedQ() {
		return countedQ;
	}

	public void setCountedQ(java.math.BigInteger countedQ) {
		this.countedQ = countedQ;
	}
    
	public java.math.BigInteger getCurrentQ() {
		return currentQ;
	}

	public void setCurrentQ(java.math.BigInteger currentQ) {
		this.currentQ = currentQ;
	}
    
	public java.math.BigInteger getAllocatedQ() {
		return allocatedQ;
	}

	public void setAllocatedQ(java.math.BigInteger allocatedQ) {
		this.allocatedQ = allocatedQ;
	}
    
	public java.math.BigInteger getOtherQ() {
		return otherQ;
	}

	public void setOtherQ(java.math.BigInteger otherQ) {
		this.otherQ = otherQ;
	}
    
	public String getLocationC() {
		return locationC;
	}

	public void setLocationC(String locationC) {
		this.locationC = locationC;
	}
    
	public String getStockTypeN() {
		return stockTypeN;
	}

	public void setStockTypeN(String stockTypeN) {
		this.stockTypeN = stockTypeN;
	}

	public String getDenialLabel() {
		return denialLabel;
	}

	public void setDenialLabel(String denialLabel) {
		this.denialLabel = denialLabel;
	}

	public BigInteger getLocationQuantity() {
		return locationQuantity;
	}

	public void setLocationQuantity(BigInteger locationQuantity) {
		this.locationQuantity = locationQuantity;
	}

	public PaginationTO getPagination() {
		return pagination;
	}

	public void setPagination(PaginationTO pagination) {
		this.pagination = pagination;
	}

	public StatusTO getStatusTO() {
		return statusTO;
	}

	public void setStatusTO(StatusTO statusTO) {
		this.statusTO = statusTO;
	}

	public PartsXWarehouseTO getPartsXWarehouse() {
		return partsXWarehouse;
	}

	public void setPartsXWarehouse(PartsXWarehouseTO partsXWarehouse) {
		this.partsXWarehouse = partsXWarehouse;
	}

	public Date getStartS() {
		return startS;
	}

	public void setStartS(Date startS) {
		this.startS = startS;
	}

	public Date getEndS() {
		return endS;
	}

	public void setEndS(Date endS) {
		this.endS = endS;
	}

	public BigInteger getBkSubDivisionUidD() {
		return bkSubDivisionUidD;
	}

	public void setBkSubDivisionUidD(BigInteger bkSubDivisionUidD) {
		this.bkSubDivisionUidD = bkSubDivisionUidD;
	}

	public String getCountryTimeZoneC() {
		return countryTimeZoneC;
	}

	public void setCountryTimeZoneC(String countryTimeZoneC) {
		this.countryTimeZoneC = countryTimeZoneC;
	}
	
}
