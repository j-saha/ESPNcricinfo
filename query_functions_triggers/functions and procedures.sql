--II
CREATE OR REPLACE FUNCTION GET_NO_OF_MATCH(UPID IN VARCHAR2)
RETURN NUMBER IS
	NUM_0F_MATCH NUMBER;
BEGIN 
	SELECT COUNT(*) INTO NUM_0F_MATCH 
	FROM UMPIRE_MATCH
	GROUP BY UMPIRE_ID
	HAVING UMPIRE_ID=UPID;
	
	RETURN NUM_0F_MATCH;

EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 0;
	WHEN OTHERS THEN 
		RETURN 0;
END;
/









--IV
CREATE OR REPLACE FUNCTION HIGHESTWICKET_IN_GROUND(GID IN VARCHAR2)
RETURN VARCHAR2 IS
	MSG VARCHAR2(100);
	PID VARCHAR2(100);
	MID VARCHAR2(100);
	NUM_WICKETS NUMBER;
BEGIN
	SELECT M.MATCH_ID,PS.PLAYER_ID,NUM_OF_WICKETS INTO MID,PID,NUM_WICKETS
	FROM MATCH M, PLAYER_SCORE PS
	WHERE M.GROUND_ID=GID AND PS.MATCH_ID=M.MATCH_ID AND
	(
	(M.MATCH_ID,PLAYER_ID)=ANY(
		SELECT M1.MATCH_ID,PLAYER_ID FROM MATCH M1, PLAYER_SCORE PS1 WHERE M1.GROUND_ID=GID AND PS1.MATCH_ID=M1.MATCH_ID AND 
		NUM_OF_WICKETS=(SELECT MAX(NUM_OF_WICKETS) FROM MATCH M2, PLAYER_SCORE PS2 WHERE M2.GROUND_ID=GID AND PS2.MATCH_ID=M2.MATCH_ID))
	);

	MSG := MID||' '||PID||' '||NUM_WICKETS;
	RETURN MSG;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 'NO DATA FOUND';
	WHEN TOO_MANY_ROWS THEN
		FOR R IN (SELECT M.MATCH_ID MI,PS.PLAYER_ID PI,NUM_OF_WICKETS
			FROM MATCH M, PLAYER_SCORE PS
			WHERE M.GROUND_ID=GID AND PS.MATCH_ID=M.MATCH_ID AND
			(
			(M.MATCH_ID,PLAYER_ID)=ANY(
				SELECT M1.MATCH_ID,PLAYER_ID FROM MATCH M1, PLAYER_SCORE PS1 WHERE M1.GROUND_ID=GID AND PS1.MATCH_ID=M1.MATCH_ID AND 
				NUM_OF_WICKETS=(SELECT MAX(NUM_OF_WICKETS) FROM MATCH M2, PLAYER_SCORE PS2 WHERE M2.GROUND_ID=GID AND PS2.MATCH_ID=M2.MATCH_ID))
			))
		LOOP
			MID := R.MI;
			PID := R.PI;
			NUM_WICKETS := R.NUM_OF_WICKETS;
		END LOOP;

		MSG := MID||' '||PID||' '||NUM_WICKETS;
		RETURN MSG;
	WHEN OTHERS THEN
		RETURN 'NO MATCH PLAYED IN THIS GROUND';
END;
/






--CHECKING A TEAM SERIES ALREADY IN TEAM SERIES TABLE
CREATE OR REPLACE FUNCTION CHECKING_TEAM_SERIES(TID IN VARCHAR2, SID VARCHAR2)
RETURN NUMBER IS
	CNT NUMBER;
BEGIN
	SELECT COUNT(*) INTO CNT
	FROM TEAM_SERIES
	WHERE TEAM_ID=TID AND SERIES_ID=SID;
	IF CNT>0 THEN
		RETURN 1;
	ELSE 	RETURN 0;
	END IF;
EXCEPTION
	WHEN OTHERS THEN 
		RETURN 0;
END;
/







--CHECKING A PLAYER ALREADY IN PLAYER STAT TABLE
CREATE OR REPLACE FUNCTION CHECKING_PLAYER_PLAYERSTAT(PID IN VARCHAR2)
RETURN NUMBER IS
	CNT NUMBER;
BEGIN
	SELECT COUNT(*) INTO CNT
	FROM PLAYER_STAT
	WHERE PLAYER_ID=PID;
	IF CNT>0 THEN
		RETURN 1;
	ELSE
		RETURN 0;
	END IF;
EXCEPTION
	WHEN OTHERS THEN
		RETURN 0;
END;
/


--HIGHESTRUN_IN_GROUD
CREATE OR REPLACE FUNCTION HIGHESTRUN_IN_GROUND(GID IN VARCHAR2)
RETURN VARCHAR2 IS
	FOUND_ID VARCHAR2(100);
BEGIN
	SELECT ID INTO FOUND_ID FROM(SELECT M.MATCH_ID AS ID, SUM(PS.SCORED_RUNS) AS RUN
	FROM MATCH M, PLAYER_SCORE PS, TEAM_PLAYER TP
	WHERE M.GROUND_ID=GID AND PS.MATCH_ID=M.MATCH_ID AND TP.PLAYER_ID=PS.PLAYER_ID
	GROUP BY M.MATCH_ID, TP.TEAM_ID) WHERE RUN=(SELECT MAX(SUM(PS.SCORED_RUNS)) AS RUN
	FROM MATCH M, PLAYER_SCORE PS, TEAM_PLAYER TP
	WHERE M.GROUND_ID=GID AND PS.MATCH_ID=M.MATCH_ID AND TP.PLAYER_ID=PS.PLAYER_ID
	GROUP BY M.MATCH_ID, TP.TEAM_ID);
	
	RETURN FOUND_ID;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 'NO DATA FOUND';
	WHEN OTHERS THEN
		RETURN 'NO MATCH PLAYED IN THIS GROUND';
END;
/







--age calculate
CREATE OR REPLACE FUNCTION CALCULATE_AGE(P_ID IN VARCHAR2)
RETURN NUMBER IS
    AGE NUMBER;
BEGIN
		SELECT MONTHS_BETWEEN(SYSDATE, DATE_OF_BIRTH)/12 INTO AGE
		FROM PERSON
		WHERE PERSON_ID=P_ID;
		RETURN AGE;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 0;
	WHEN OTHERS THEN 
		RETURN 0;
end;
/








CREATE OR REPLACE FUNCTION SIXES_IN_SERIES(S_ID IN VARCHAR2)
RETURN NUMBER IS
	NUM NUMBER;
BEGIN
	SELECT SUM(NUM_OF_SIXES) INTO NUM
	FROM MATCH M, PLAYER_SCORE PS
	WHERE M.MATCH_ID=PS.MATCH_ID AND M.SERIES_ID=S_ID;
	
	RETURN NUM;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
		RETURN 0;
	WHEN OTHERS THEN 
		RETURN 0;
END;
/





CREATE OR REPLACE PROCEDURE GET_FULLNAME_FROM_PERSON(P_ID IN VARCHAR2, FULLNAME OUT VARCHAR2) IS
	F_NAME VARCHAR2(50);
	L_NAME VARCHAR2(50);
BEGIN 
	SELECT FIRST_NAME, LAST_NAME INTO F_NAME, L_NAME FROM PERSON
	WHERE PERSON_ID=P_ID;
	FULLNAME:=F_NAME||' '||L_NAME;
	
EXCEPTION
	WHEN OTHERS THEN 
		FULLNAME:='NO_DATA_FOUND';
END;
/
CREATE OR REPLACE PROCEDURE PROC_FOURS_IN_SERIES(SID IN VARCHAR2, CNT OUT NUMBER) IS
	
BEGIN
	SELECT SUM(NUM_OF_FOURS) INTO CNT
	FROM PLAYER_SCORE PS, MATCH M
	WHERE M.SERIES_ID=SID AND M.MATCH_ID=PS.MATCH_ID;
END;



































